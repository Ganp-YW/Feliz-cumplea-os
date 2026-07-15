import flet as ft
import random
from database import obtener_todos_los_mensajes

mensajes_disponibles_global = []

def main(page: ft.Page):
    page.title = "El Frasco Virtual"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 30
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 700

    global mensajes_disponibles_global
    
    if not mensajes_disponibles_global:
        todos_los_mensajes = obtener_todos_los_mensajes()
        random.shuffle(todos_los_mensajes)
        mensajes_disponibles_global = todos_los_mensajes

    # Contenedor para mostrar el mensaje
    mensaje_texto = ft.Text("Presiona el botón para sacar un mensaje del frasco", 
                            text_align=ft.TextAlign.CENTER, 
                            size=18,
                            color=ft.Colors.BLACK87)
                            
    categoria_texto = ft.Text("", 
                              size=14, 
                              weight=ft.FontWeight.BOLD,
                              color=ft.Colors.WHITE)

    tarjeta_mensaje = ft.Container(
        content=ft.Column(
            [categoria_texto, mensaje_texto],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        padding=30,
        bgcolor=ft.Colors.GREY_200,
        border_radius=20,
        width=300,
        height=200,
        alignment=ft.Alignment.CENTER,
        animate=ft.Animation(500, ft.AnimationCurve.EASE_OUT)
    )

    def sacar_mensaje(e):
        # Efecto de carga o agitación leve del frasco (opcional)
        boton_frasco.icon_color = ft.Colors.BLUE_700
        page.update()
        
        global mensajes_disponibles_global
        
        # Si la lista se agotó, volvemos a descargar y barajar
        if not mensajes_disponibles_global:
            todos_los_mensajes = obtener_todos_los_mensajes()
            random.shuffle(todos_los_mensajes)
            mensajes_disponibles_global = todos_los_mensajes
            
        if mensajes_disponibles_global:
            mensaje = mensajes_disponibles_global.pop(0)
            
            texto = mensaje["texto"]
            categoria = mensaje["categoria"]
            color_nombre = mensaje["color"]
            
            # Mapear color simple a color de Flet
            color_map = {
                "red": ft.Colors.RED_200,
                "blue": ft.Colors.BLUE_200,
                "green": ft.Colors.GREEN_200,
                "yellow": ft.Colors.YELLOW_200
            }
            
            bgcolor = color_map.get(color_nombre, ft.Colors.GREY_200)
            
            # Actualizar la tarjeta
            tarjeta_mensaje.bgcolor = bgcolor
            mensaje_texto.value = f'"{texto}"'
            categoria_texto.value = categoria.upper()
            categoria_texto.color = ft.Colors.BLACK54
            
        boton_frasco.icon_color = ft.Colors.BLUE_400
        page.update()

    # Botón que simula el frasco
    boton_frasco = ft.IconButton(
        icon=ft.Icons.CHEVRON_RIGHT_ROUNDED, # Placeholder temporal, lo cambiamos a un jar o regalo
        icon_size=100,
        icon_color=ft.Colors.BLUE_400,
        on_click=sacar_mensaje,
        tooltip="Sacar un mensaje"
    )
    
    boton_frasco.icon = ft.Icons.VOLCANO # O algo parecido a un frasco. Flet tiene muchos iconos. MEJOR: usar un icono de caja de regalo o corazón
    boton_frasco.icon = ft.Icons.FAVORITE
    boton_frasco.icon_color = ft.Colors.PINK_400

    # Etiqueta debajo del frasco
    instruccion = ft.Text("Toca el corazón para abrir el frasco", size=16, color=ft.Colors.GREY_700)

    # Añadir todo a la página
    page.add(
        ft.Column(
            [
                tarjeta_mensaje,
                ft.Container(height=50), # Espaciador
                ft.Row(
                    [
                        ft.Image(src="gato.png", width=80, height=80, fit=ft.BoxFit.CONTAIN),
                        boton_frasco,
                        ft.Image(src="coneja.png", width=80, height=80, fit=ft.BoxFit.CONTAIN)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                ),
                instruccion
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.run(main)
