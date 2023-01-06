from pytezos import MichelsonScript

def run_michelson_code(script):    
    """Run michelson code and returns the result of the execution
    
    Keyword arguments:
    script (str) -- String containing the michelson code to run
    Return: String containing the output resulting from the michelson code execution
    """
    michelson_script = MichelsonScript(script)

    result = michelson_script.execute()

    return result
