from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError

from config import ServerConfig

style = style_from_dict({
    Token.QuestionMark: "#E91E63 bold",
    Token.Selected: "#14B850 bold",
    Token.Instruction: "",
    Token.Answer: "#14B850 bold",
    Token.Question: "",
})

class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text, 16)
        except ValueError:
            raise ValidationError(
                message="Please enter a number",
                cursor_position=len(document.text))

class P4RuntimeClient():

    def __init__(self):
        # Configure the host and the port to which the client should connect to.
        self.host = ServerConfig.HOST
        self.server_port = ServerConfig.SERVER_PORT

        with open(ServerConfig.SERVER_CERTIFICATE, "rb") as file:
            trusted_certs = file.read()
        
        # Instantiate a communication channel and bind the client to the server.
        self.credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
        self.channel = grpc.secure_channel("{}:{}".format(self.host, self.server_port), self.credentials)
        self.stub = p4runtime_pb2_grpc.P4RuntimeStub(self.channel)

    def CLI_PMA_init_database():
        return self.stub.CLI_PMA_init_database()

    def CLI_PMA_load_switch_data(switch_name, dir_path, switch_id, switch_dat_file, table_defines_file):
        return self.stub.CLI_PMA_load_switch_data(switch_name, dir_path, switch_id, switch_dat_file, table_defines_file)

    def CLI_PMA_load_switch_modules(switch_name, dir_path, switch_id):
        return self.stub.CLI_PMA_load_switch_modules(switch_name, dir_path, switch_id)

    def CLI_PMA_load_reg_data(switch_id, extern_defines_file):
        return self.stub.CLI_PMA_load_reg_data(switch_id, extern_defines_file)

    def CLI_PMA_load_libsume_module(lib_path):
        return self.stub.CLI_PMA_load_libsume_module(lib_path)

def main():
    client = P4RuntimeClient()

    paramsPMA_load_switch_data = [
    {
        "type": "input",
        "name": "switch_name",
        "message": "load_switch_data(switch_name, ..., ..., ..., ...):"
    },
    {
        "type": "input",
        "name": "dir_path",
        "message": "load_switch_data(..., dir_path, ..., ..., ...):"
    },
    {
        "type": "input",
        "name": "switch_id",
        "message": "load_switch_data(..., ..., switch_id, ..., ...):",
        "validate": NumberValidator,
        "filter": lambda val: int(val, 16)
    },
    {
        "type": "input",
        "name": "switch_dat_file",
        "message": "load_switch_data(..., ..., ..., switch_dat_file, ...):"
    },
    {
        "type": "input",
        "name": "table_defines_file",
        "message": "load_switch_data(..., ..., ..., ..., table_defines_file):"
    }
    ]

    paramsPMA_load_switch_modules = [
    {
        "type": "input",
        "name": "switch_name",
        "message": "load_switch_modules(switch_name, ..., ...):"
    },
    {
        "type": "input",
        "name": "dir_path",
        "message": "load_switch_modules(..., dir_path, ...):"
    },
    {
        "type": "input",
        "name": "switch_id",
        "message": "load_switch_modules(..., ..., switch_id):",
        "validate": NumberValidator,
        "filter": lambda val: int(val, 16)
    }
    ]

    paramsPMA_load_reg_data = [
    {
        "type": "input",
        "name": "switch_id",
        "message": "load_reg_data(switch_id, ...)",
        "validate": NumberValidator,
        "filter": lambda val: int(val, 16)
    },
    {
        "type": "input",
        "name": "extern_defines_file",
        "message": "load_reg_data(..., extern_defines_file)"
    }
    ]

    paramsPMA_load_libsume_module = [
    {
        "type": "input",
        "name": "lib_path",
        "message": "load_libsume_module(lib_path)",
    }
    ]

    optionQ = [
        {
            "type": "list",
            "name": "action",
            "message": "What to do:",
            "choices": ["PMA - init_database()", 
                        "PMA - load_switch_data()", 
                        "PMA - load_switch_modules()", 
                        "PMA - load_reg_data()", 
                        "PMA - load_libsume_module()", 
                        "Exit"]
        }
    ]

    optC = prompt(optionQ, style=style)
    while optC["action"] != "Exit":
        if optC["action"] == "PMA - init_database()":
            #call_result = client.CLI_PMA_init_database()
            call_result = True
            if call_result == True:
                print "init_database() -> Success!"
            else:
                print "init_database() -> Fail!"

        elif optC["action"] == "PMA - load_switch_data()":
            answers = prompt(paramsPMA_load_switch_data, style=style)

            switch_name = answers["switch_name"]
            dir_path = answers["dir_path"]
            switch_id = answers["switch_id"]
            switch_dat_file = answers["switch_dat_file"]
            table_defines_file = answers["table_defines_file"]

            #call_result = client.CLI_PMA_load_switch_data(switch_name, dir_path, switch_id, switch_dat_file, table_defines_file)
            call_result = True
            if call_result == True:
                print "load_switch_data() -> Success!"
            else:
                print "load_switch_data() -> Fail!"

        elif optC["action"] == "PMA - load_switch_modules()":
            answers = prompt(paramsPMA_load_switch_modules, style=style)

            switch_name = answers["switch_name"]
            dir_path = answers["dir_path"]
            switch_id = answers["switch_id"]

            #call_result = client.CLI_PMA_load_switch_modules(switch_name, dir_path, switch_id)
            call_result = True
            if call_result == True:
                print "load_switch_modules() -> Success!"
            else:
                print "load_switch_modules() -> Fail!"

        elif optC["action"] == "PMA - load_reg_data()":
            answers = prompt(paramsPMA_load_reg_data, style=style)

            switch_id = answers["switch_id"]
            extern_defines_file = answers["extern_defines_file"]

            #call_result = client.CLI_PMA_load_reg_data(switch_id, extern_defines_file)
            call_result = True
            if call_result == True:
                print "load_reg_data() -> Success!"
            else:
                print "load_reg_data() -> Fail!"

        elif optC["action"] == "PMA - load_libsume_module()":
            answers = prompt(paramsPMA_load_libsume_module, style=style)

            lib_path = answers["lib_path"]

            #call_result = client.CLI_PMA_load_libsume_module(lib_path)
            call_result = True
            if call_result == True:
                print "load_libsume_module() -> Success!"
            else:
                print "load_libsume_module() -> Fail!"

        optC = prompt(optionQ, style=style)

if __name__ == "__main__":
    main()
