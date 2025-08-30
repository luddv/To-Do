import flet

from flet import (
    Checkbox,
    Column,
    IconButton,
    OutlinedButton,
    Page,
    Row,
    Tab,
    Tabs,
    Text,
    TextField,
    Colors,
    Icons,
    TextThemeStyle,
)  # Importação dos componentes que vão ser utilizados na aplicação


# Componente de tarefa
class Task(Column):
    def __init__(self, name, on_status_change, on_delete):
        super().__init__()
        self.name = name
        self.on_status_change = on_status_change
        self.on_delete = on_delete
        self.completed = False

        self.checkbox = Checkbox(label=self.name, value=False, on_change=self.status_changed)
        self.edit_field = TextField(value=self.name, expand=True)

        self.display_view = Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.checkbox,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=Icons.CREATE_OUTLINED,
                            tooltip="Editar",
                            on_click=self.edit_clicked,
                            icon_color=Colors.BLUE,
                        ),
                        IconButton(
                            icon=Icons.DELETE_OUTLINED,
                            tooltip="Excluir",
                            on_click=self.delete_clicked,
                            icon_color=Colors.RED,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.edit_field,
                IconButton(
                    icon=Icons.DONE_OUTLINE_OUTLINED,
                    tooltip="Salvar",
                    icon_color=Colors.GREEN,
                    on_click=self.save_clicked,
                ),
            ],
        )

        self.controls = [self.display_view, self.edit_view]

    def edit_clicked(self, e):
        self.edit_field.value = self.checkbox.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.checkbox = Checkbox(label=self.edit_field.value, value=self.completed, on_change=self.status_changed)
        self.display_view.controls[0] = self.checkbox
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def delete_clicked(self, e):
        self.on_delete(self)

    def status_changed(self, e):
        self.completed = self.checkbox.value
        self.on_status_change(self)


# Aplicativo principal
class TodoApp(Column):
    def __init__(self):
        super().__init__()
        self.new_task = TextField(
            hint_text="Digite uma nova tarefa...",
            expand=True,
            on_submit=self.add_task,
        )

        self.task_list = Column()
        self.filter_tabs = Tabs(
            selected_index=0,
            on_change=self.filter_changed,
            tabs=[
                Tab(text="Todas"),
                Tab(text="Ativas"),
                Tab(text="Concluídas"),
            ],
        )

        self.task_counter = Text("0 tarefas ativas")

        self.controls = [
            Text("Tarefas", style=TextThemeStyle.HEADLINE_MEDIUM),
            Row(controls=[self.new_task]),
            self.filter_tabs,
            self.task_list,
            Row(
                alignment="spaceBetween",
                controls=[
                    self.task_counter,
                    OutlinedButton(
                        text="Limpar concluídas",
                        on_click=self.clear_completed,
                    ),
                ],
            ),
        ]

    def add_task(self, e):
        name = self.new_task.value.strip()
        if name:
            task = Task(name, self.task_status_changed, self.delete_task)
            self.task_list.controls.append(task)
            self.new_task.value = ""
            self.new_task.focus()
            self.update()

    def task_status_changed(self, task):
        self.update()

    def delete_task(self, task):
        self.task_list.controls.remove(task)
        self.update()

    def clear_completed(self, e):
        for task in self.task_list.controls[:]:
            if task.completed:
                self.delete_task(task)

    def filter_changed(self, e):
        self.update()

    def update(self):
        selected = self.filter_tabs.tabs[self.filter_tabs.selected_index].text
        active_count = 0
        for task in self.task_list.controls:
            task.visible = (
                selected == "Todas"
                or (selected == "Ativas" and not task.completed)
                or (selected == "Concluídas" and task.completed)
            )
            if not task.completed:
                active_count += 1
        self.task_counter.value = f"{active_count} tarefas ativas"
        super().update()


# Função principal
def main(page: Page):
    page.title = "Tarefas"
    page.scroll = "adaptive"
    page.horizontal_alignment = "center"
    page.add(TodoApp())

flet.app(target=main)