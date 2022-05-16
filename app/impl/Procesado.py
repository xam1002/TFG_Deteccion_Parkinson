from shutil import ExecError
from tqdm import tqdm
import cv2
import scipy.signal
import numpy as np
import pandas as pd
import mediapipe as mp
import joblib
import os
import glob
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

class Procesado:

    def obtener_numero_fotogramas(vd):
        vc = cv2.VideoCapture(vd)
        i = 0
        if (vc.isOpened()==False):
            print("Error")
        else:
            while(True):
                if not vc.read()[0]:
                    break
                i+=1
        return i
    
    def frameVideo(vd):
        vc = cv2.VideoCapture(vd)

        if (vc.isOpened()==False):
            print("Error")
        else:
            while(vc.isOpened()):
                ret,frame = vc.read()
                if ret:
                    yield frame
                else:
                    vc.release()

    def frameMano(self, frame, static=True,max_num_hands=1,min_detection_confidence=0):
        with mp_hands.Hands(static_image_mode=static,max_num_hands=max_num_hands, min_detection_confidence=min_detection_confidence) as hands:
            results = hands.process(cv2.flip(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 1))
            annotated_frame = cv2.flip(frame.copy(), 1)
            
            if results.multi_hand_landmarks is None:
                return None
                
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(annotated_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            return results.multi_hand_landmarks
    
    def calcularDistancia(mano):
        x4=mano[0].landmark[4].x
        y4=mano[0].landmark[4].y
        x8=mano[0].landmark[8].x
        y8=mano[0].landmark[8].y
        
        if x4<0 or y4<0 or x8<0 or y8<0:
            return None
        
        p4=np.array((x4,y4))
        p8=np.array((x8,y8))
        
        return np.linalg.norm(p4-p8)
    
    def calcularDistanciasVideo(self, manos):
        dist = []
        for i in manos:
            if i is not None:
                dist.append(self.calcularDistancia(i))
            
        return dist

    def analizarVideo(self, ruta, debug = False):
        manos=[]
        if debug:
            num = self.obtener_numero_fotogramas(ruta)
            carga = tqdm(total = num, position = 0, leave = False)
        for k, i in enumerate(self.frameVideo(ruta)):
            manos.append(self.frameMano(self, i))
            if debug:
                carga.set_description("Procesando fotogramas...".format(k))
                carga.update(1)
        if debug:
            carga.close() 
        dist = self.calcularDistanciasVideo(self, manos)
        dist = scipy.signal.savgol_filter(dist, 3, 1)

        return dist
    
    def obtener_amplitudes(self, datos):
        maximos=[]
        minimos=[]
        salir = False
        i = 1
        media = np.mean(datos)
        for f in range(10):
            min_actual = float('inf')
            max_actual = 0
            if f == 5:
                i = -1
            while datos[i] > media:
                if f == 5:
                    i-=1
                else:
                    i+=1
            while datos[i] > media or not salir:
                if datos[i] < media and datos[i] < min_actual:
                    min_actual = datos[i] 
                if datos[i] > media:
                    salir = True
                    if datos[i] > max_actual:
                        max_actual = datos[i]
                if f >= 5:
                    i-=1
                else:
                    i+=1
            salir = False
            
            maximos.append(max_actual)
            minimos.append(min_actual)

        return maximos, minimos
      
    def obtener_tiempos(datos, maximos, minimos):
        mini = []
        maxi = []
        for a in range(10):
            mini.append(list(datos).index(minimos[a]))
            maxi.append(list(datos).index(maximos[a]))

        resta = []
        for m1, m2 in zip(mini,maxi):
            resta.append(abs(m1-m2))
        
        return resta

    def obtener_velocidades(diferencias, tiempos):
        velocidades=[]
        for d,t in zip(diferencias, tiempos):
            velocidades.append(d/t)

        return velocidades

    def normalizacion(lista, maximo, minimo):
        norm = []
        p = 0
        for l in range(len(lista)):
            if l % 10 == 0 and l != 0:
                p+=1
            norm.append((lista[l] - minimo) / (maximo - minimo))
        return norm

    @classmethod
    def realizar_prediccion(self, ruta, mano, sexo, debug):
        columnas = ['Max1. norm.', 'Max2. norm.', 'Max3. norm.', 'Max4. norm.', 'Max5. norm.', 
                    'Max6. norm.', 'Max7. norm.', 'Max8. norm.', 'Max9. norm.', 'Max10. norm.', 'Min1. norm.', 
                    'Min2. norm.', 'Min3. norm.', 'Min4. norm.', 'Min5. norm.', 'Min6. norm.', 'Min7. norm.', 
                    'Min8. norm.', 'Min9. norm.', 'Min10. norm.', 'Diff1. norm.', 'Diff2. norm.', 'Diff3. norm.', 
                    'Diff4. norm.', 'Diff5. norm.', 'Diff6. norm.', 'Diff7. norm.', 'Diff8. norm.', 'Diff9. norm.', 
                    'Diff10. norm.', 'Mean speed', 'Hand R(0)/L(1)', 'Sex M(0)/W(1)']
        
        nombre_modelo = ""
        borrar = False
        for g in glob.glob('..//Flask//app//modelo//*'):
            if ".pkl" in g.split("//")[-1].split("\\")[-1] and not borrar:
                nombre_modelo = g.split("//")[-1].split("\\")[-1]
                borrar = True
            else:
                os.remove(g)
        try:
            modelo = joblib.load('..//Flask//app//modelo//' + nombre_modelo)
        except (IndexError, EOFError):
            raise Exception("El modelo no es válido")

        datos = self.analizarVideo(self, ruta, debug)
        maximos, minimos = self.obtener_amplitudes(self, datos)
        tiempos = self.obtener_tiempos(datos, maximos, minimos)

        max_norm = self.normalizacion(maximos, max(maximos), min(minimos))
        min_norm = self.normalizacion(minimos, max(maximos), min(minimos))
        dif_norm = []
        for n1,n2 in zip(max_norm, min_norm):
            dif_norm.append(n1-n2)
        velocidades = self.obtener_velocidades(dif_norm, tiempos)

        lista=[]
        lista.extend(max_norm)
        lista.extend(min_norm)
        lista.extend(dif_norm)
        lista.append(np.mean(velocidades))
        lista.append(mano)
        lista.append(sexo)
        df = pd.DataFrame(data = [lista], columns=columnas)

        return modelo.predict(df)