import pygame,sys,random
from pygame.math import Vector2

pygame.init()
ancho=800
alto=400


ventana = pygame.display.set_mode((ancho,alto))      ##variable que guarda el tamaño de la pantalla
pygame.display.set_caption("SNAKE")               ##Se utiliza para aplicar el nombre en la ventana

class Serpiente():                                ##Se utiliza para crear la posicion de la serpiente
    def __init__(self):
        self.Cuerpo= [Vector2(20,100),Vector2(20,110),Vector2(20,120)]
        self.direccion= Vector2(0,-20)              ##la direccion inicial donde se mueve la serpiente
        self.food= False

    def Dibujar(self):                            ##se dibuja el cuerpo con un rectangulo (donde se dibuja,color,tamaño)
        for bloque in self.Cuerpo:
            pygame.draw.rect(ventana,(0,255,0),(bloque.x,bloque.y,20,20))

    def Movimiento(self):                       ##[0,1,2]-->[0,1]-->[None,0,1]-->[-1,0,1]logica detras del movimiento
        if self.food == True:
            CopiaCuerpo = self.Cuerpo
            CopiaCuerpo.insert(0,CopiaCuerpo[0]+self.direccion)        ## actualiza el movimiento en caso de que haya
            self.Cuerpo = CopiaCuerpo[:]                               ## comido una manzana agregando un segmento mas
            self.food = False
        else:
            CopiaCuerpo = self.Cuerpo[:-1]
            CopiaCuerpo.insert(0, CopiaCuerpo[0] + self.direccion)      ## redibuja el rectangulo adelante borrando
            self.Cuerpo = CopiaCuerpo[:]                                ## el rectangulo anterior e insertando uno nuevo



    def movi_up(self):
        self.direccion = Vector2(0,-20)
    def movi_down(self):
        self.direccion = Vector2(0,20)
    def movi_right(self):
        self.direccion = Vector2(20,0)
    def movi_left(self):
        self.direccion = Vector2(-20,0)

    def die(self):                     ## indica que si choca con los lados de la pantalla Muere (800 ancho 400 largo)
        if self.Cuerpo[0].x >= ancho+20 or self.Cuerpo[0].y >= alto+20 or self.Cuerpo[0].x <= -20 or self.Cuerpo[0].y <= -20:
            return True
        for i in self.Cuerpo[1:]:
            if self.Cuerpo[0] == i:
                return True

class Manzana:
    def __init__(self):
        self.Generar()

    def DibujarM(self):                          ## Dibuja la manzana
        pygame.draw.rect(ventana,(255,0,0),(self.pos.x,self.pos.y,+20,+20))
    def Generar(self):                                  ## Genera la manzana en base entera par por eso se divide
        ancho2=ancho-100
        alto2=alto-100
        self.x = random.randrange(0,ancho2//20)     ## en un lugar aleatorio pero dentro de la pantalla
        self.y = random.randrange(0, alto2//20 )
        self.pos= Vector2(self.x*20, self.y*20)

    def Colision(self,serpiente):            ## Calcula la pocicion de la comida y el cuerpo si es asi aumenta 1 mas
        if serpiente.Cuerpo[0] == self.pos:
            self.Generar()
            Serpiente.food = True

            return True

        for bloque in serpiente.Cuerpo[1:]:  ##permite que la serpiente no se haga danio a si misma,caleando la funcion
            if self.pos == bloque:           ## del tamanio de su cuerpo y si es igual pum F
                    self.Generar()

        return False




def main():                                         ## Metodo principal que ejecuta el bucle (el juego en si)
    SP = Serpiente()                                ## El objeto
    MZ= Manzana()                                   ## El objeto a comer
    Puntos=0
    fps= pygame.time.Clock()                        ## limita los fps (clase que controla FPS)



    while True:
        fps.tick(10)                                ## limita el movimiento a 30 fps



        for event in pygame.event.get():            ##Cuando ocurre un evento...
            if event.type == pygame.QUIT:           ##Si el evento es cerrar la ventana
                pygame.quit()                       ##Se cierra pygame
                sys.exit()                          ##Se cierra el programa
            if event.type == pygame.KEYDOWN and SP.direccion.y != 20:
                if event.key == pygame.K_UP:        ##Define que pasa si toca una tecla (en este caso arriba)
                    SP.movi_up()

            if event.type == pygame.KEYDOWN and SP.direccion.y != -20:
                if event.key == pygame.K_DOWN:      ##define que pasa si toca una tecla (en este caso abajo)
                    SP.movi_down()

            if event.type == pygame.KEYDOWN and SP.direccion.x != -20:
                if event.key == pygame.K_RIGHT:
                    SP.movi_right()

            if event.type == pygame.KEYDOWN and SP.direccion.x != 20:
                if event.key == pygame.K_LEFT:
                    SP.movi_left()




        ventana.fill((0,250,255))                       ##Pinta la pantalla de negro
        SP.Dibujar()                                ##se llama a dibujo (onda dibuja la serpinete)
        SP.Movimiento()                             ##se llama a el movimiento de la serpiente
        if SP.die():                                ##se llama a la funcion morir
            quit()
        MZ.DibujarM()                               ##sel lama a la funcion dibujar que crea al a manzana
        if MZ.Colision(SP):                         ##puntaje usando acumulador
            Puntos+=1
        pygame.display.update()                     ## Actualiza la pantalla
main()

