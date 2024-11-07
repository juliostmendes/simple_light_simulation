import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront
import tkinter as tk
from tkinter import ttk

cena = pywavefront.Wavefront("objetos/sphere.obj", create_materials=True, collect_faces=True, parse=True)
#cena = pywavefront.Wavefront("objetos/tree.obj", create_materials=True, collect_faces=True, parse=True)
#cena = pywavefront.Wavefront("objetos/CartoonTree.obj", create_materials=True, collect_faces=True, parse=True)
#cena = pywavefront.Wavefront("objetos/medieval house.obj", create_materials=True, collect_faces=True, parse=True)


pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
glEnable(GL_DEPTH_TEST)

# Perspectivas
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glTranslatef(0.0, 0.0, -5)  # Zoom (-5 sphere, -8 tree, -15 CartoonTree, -25 medieva house)

# Variáveis de controle de iluminação
ativar_difuso = None
ativar_especular = None
ativar_suavizar = None
luz_x = None
luz_y = None
luz_z = None

# Função da luz difusa e especular iluminação
def iluminacao():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    # Configuração de posição da luz com base nos valores dos sliders
    posicao_luz = [luz_x.get(), luz_y.get(), luz_z.get(), 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, posicao_luz)

    # Aplicar flat shading para a luz difusa
    if ativar_difuso.get():
        cor_difuso = [0.6, 0.3, 0.7, 1.0]
    else:
        cor_difuso = [0.0, 0.0, 0.0, 1.0]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, cor_difuso)


    if ativar_especular.get():
        cor_especular = [0.5, 0.5, 0.5, 1.0]
        
    else:
        cor_especular = [0.0, 0.0, 0.0, 1.0]
    glLightfv(GL_LIGHT0, GL_SPECULAR, cor_especular)


    if ativar_suavizar.get():
        glShadeModel(GL_SMOOTH)
    else:
        glShadeModel(GL_FLAT)
    
    # Configuração do material com menor brilho para absorver mais luz
    glMaterialfv(GL_FRONT, GL_SPECULAR, cor_especular)
    glMaterialf(GL_FRONT, GL_SHININESS, 90.0)  # Reduz o brilho para absorver mais luz


def desenhar():
    for name, mesh in cena.meshes.items():
        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            for vertex_i in face:
                glVertex3fv(cena.vertices[vertex_i])
        glEnd()

# Tela Tkinter
def controle_luz():
    global ativar_difuso, ativar_especular, ativar_suavizar, luz_x, luz_y, luz_z
    
    root = tk.Tk()
    root.title("Controles de Iluminação")
    root.geometry("300x180")
    
    ativar_difuso = tk.BooleanVar(value=True)
    ativar_especular = tk.BooleanVar(value=True)
    ativar_suavizar = tk.BooleanVar(value=True)
    luz_x = tk.DoubleVar(value=1.0)
    luz_y = tk.DoubleVar(value=1.0)
    luz_z = tk.DoubleVar(value=1.0)

    
    tk.Label(root, text="Posição da Luz - X").pack()
    ttk.Scale(root, from_=-10, to=10, variable=luz_x).pack()

    tk.Label(root, text="Posição da Luz - Y").pack()
    ttk.Scale(root, from_=-10, to=10, variable=luz_y).pack()

    tk.Label(root, text="Posição da Luz - Z").pack()
    ttk.Scale(root, from_=-5, to=16, variable=luz_z).pack()

    ttk.Checkbutton(root, text="Luz Difusa", variable=ativar_difuso).pack()
    ttk.Checkbutton(root, text="Luz Especular", variable=ativar_especular).pack()
    ttk.Checkbutton(root, text="Suavizar", variable=ativar_suavizar).pack()
    
    def update():
        root.update_idletasks()
        root.update()

    return update

# Função principal de execução do PyGame e OpenGL
def main():
    
    atualizar_controles = controle_luz()

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Configuração da iluminação com base nos parâmetros
        iluminacao()
        
        # Limpeza dos buffers de cor e profundidade
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        
        #glRotatef(1, 0, 1, 0)  

        # Renderização do objeto carregado
        glPushMatrix()
        desenhar() 
        glPopMatrix()

        # Atualização da tela
        pygame.display.flip()
        #clock.tick(60)  # Limitar a 60 FPS

        # Atualizar a interface de controles
        atualizar_controles()

# Executar o programa
main()
