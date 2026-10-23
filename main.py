
import flet as ft
from flet.controls import alignment
from flet.controls.core import icon

from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    def handler_plus(e):
        count = 0
        count = float(input_value.value)
        count += 1
        input_value.value = count
        page.update()

    def handler_minus(e):
        count = 0
        count = int(input_value.value)
        count -= 1
        input_value.value = count
        page.update()

    # TODO
    input_tipo = ft.TextField(label="Tipo")
    input_marca= ft.TextField(label="Marca")
    input_anno= ft.TextField(label="Anno di acquisto")

    MyBtnplus= ft.IconButton(icon=ft.Icons.ADD, on_click=handler_plus, icon_color=ft.Colors.GREEN)
    MyBtnmin=  ft.IconButton(icon=ft.Icons.REMOVE,on_click=handler_minus, icon_color=ft.Colors.RED)
    input_value= ft.TextField(value="0" , width=50, height=50)




    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def aggiunta():
        if not input_anno.value.isdigit():
            alert.show_alert("l'anno non è un valore numerico")
        if not input_value.value.isdigit():
            alert.show_alert("Il valore del strumento non è un valore numerico")

        deposito.aggiungi_strumento(input_tipo.value, input_marca.value, input_anno.value,input_value.value)
        input_tipo.value=""
        input_marca.value=""
        input_anno.value=""
        input_value.value=""
        aggiorna_lista_strumenti()
        page.update()

    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento


    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    # TODO
    pulsante = ft.Button("Aggiungi Strumento", on_click=aggiunta)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Divider(),
        ft.Text("Aggiungi nuovo strumento", size=20),
        ft.Row(spacing=25,
               controls=[input_tipo, input_marca, input_anno,MyBtnmin,input_value,MyBtnplus],
               alignment=ft.MainAxisAlignment.CENTER),
        pulsante,


        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
