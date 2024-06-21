"""
WARNING:

Please make sure you install the bot with `pip install -e .` in order to get all the dependencies
on your Python environment.

Also, if you are using PyCharm or another IDE, make sure that you use the SAME Python interpreter
as your IDE.

If you get an error like:
```
ModuleNotFoundError: No module named 'botcity'
```

This means that you are likely using a different Python interpreter than the one used to install the bot.
To fix this, you can either:
- Use the same interpreter as your IDE and install your bot with `pip install --upgrade -r requirements.txt`
- Use the same interpreter as the one used to install the bot (`pip install --upgrade -r requirements.txt`)

Please refer to the documentation for more information at https://documentation.botcity.dev/
"""

# Import for the Desktop Bot
from botcity.core import DesktopBot, Backend

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = DesktopBot()
    bot.browse("http://www.botcity.dev")

    #Executando o aplicativo Sicalc
    app_path = r"C:\Program Files (x86)\Programas RFB\Sicalc Auto Atendimento\SicalcAA.exe"
    
    bot.execute(app_path)

    bot.connect_to_app(backend=Backend.WIN_32, path=app_path)
    

    #Identificando o pop-up na tela inicial
    janela_esclarecimento = bot.find_app_window(title="Esclarecimento ao Contribuinte")
    
    btn_continuar = bot.find_app_element(from_parent_window=janela_esclarecimento, title="&Continuar", class_name="ThunderRT6CommandButton")
    btn_continuar.click()


    #Selecionando a opcção do menu
    janela_principal = bot.find_app_window(title="Sicalc Auto Atendimento", class_name="ThunderRT6MDIForm")

    janela_principal.menu_select("Funções -> Preenchimento de DARF")


    #Preenchendo formulário incial
    darf = bot.find_app_element(from_parent_window=janela_principal, title="Preenchimento de DARF", class_name="ThunderRT6FormDC")
    
    darf.Edit3.type_keys("5629")

    darf.type_keys("{TAB}")
    
    
    #Preenchendo dados da DARF
    janela_principal = bot.find_app_window(title_re="Sicalc Auto Atendimento", class_name="ThunderRT6MDIForm")
    form_darf = bot.find_app_element(from_parent_window=janela_principal, title="Receita", class_name="ThunderRT6Frame")
    form_darf.type_keys("{TAB}")

    form_darf.Edit4.type_keys("310120")
    bot.wait(2000)
    form_darf.type_keys("{TAB}")

    bot.wait(2000)
    form_darf.Edit5.type_keys("10000")

    form_darf.type_keys("{ENTER}")

    form_darf.type_keys("%{f}")


    #Preenchendo formulario final
    form_darf = bot.find_app_window(title="Preenchimento DARF Auto Atendimento", class_name="ThunderRT6FormDC")
    
    form_darf.Edit5.type_keys("Petrobras")

    form_darf.Edit6.type_keys("1199991234")

    form_darf.Edit11.type_keys("33000167000101")

    form_darf.Edit10.type_keys("0")

    #Salvando arquivo PDF
    btn_imprimir = bot.find_app_element(from_parent_window=form_darf, title="&Imprimir", class_name="ThunderRT6CommandButton")
    btn_imprimir.click()

    save = bot.find_app_window(title="Salvar Saída de Impressão como")
    save.type_keys("DARF2")
    save.type_keys("{ENTER}")

    form_darf.type_keys("%{F4}")


    

    # Uncomment to mark this task as finished on BotMaestro
    # maestro.finish_task(
    #     task_id=execution.task_id,
    #     status=AutomationTaskFinishStatus.SUCCESS,
    #     message="Task Finished OK."
    # )

def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()