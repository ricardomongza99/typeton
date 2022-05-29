from src.compiler.code_generator.type import Quad, OperationType
from src.compiler.errors import CompilerEvent
from src.utils.observer import Publisher, Subscriber, Event


class FunctionActions(Publisher, Subscriber):
    def __init__(self, quad_list):
        super().__init__()

        self.parameter_counter = 0
        self.quad_list = quad_list

    def handle_event(self, event: Event):
        if event.type_ is CompilerEvent.GEN_END_FUNC:
            self.generate_end_function()
        elif event.type_ is CompilerEvent.GO_TO_MAIN:
            self.generate_go_to_main()

    def generate_end_function(self):
        quad = Quad(operation=OperationType.ENDFUNC)
        self.quad_list.append(quad)

    def generate_go_to_main(self):
        quad = Quad(operation=OperationType.GOTOMAIN)
        self.quad_list.append(quad)
