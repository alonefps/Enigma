# Rotor class represents a single rotor in the Enigma machine
class Rotor:
    def __init__(self, wiring, notch, ring_setting=0, offset=0):
        self.input_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Input alphabet for the rotor
        self.output_alphabet = wiring  # The substitution wiring for the rotor
        self.notch = notch  # The notch position for turnover
        self.ring_setting = ring_setting  # The initial position of the ring
        self.offset = offset  # The initial position of the rotor

    # Forward substitution - input letter to encrypted letter
    def substitute_forward(self, char):
        if char in self.input_alphabet:
            idx = (self.input_alphabet.index(char) +
                   self.offset - self.ring_setting) % 26
            encrypted_char = self.output_alphabet[idx]
            return encrypted_char
        return char

    # Backward substitution - encrypted letter to input letter
    def substitute_backward(self, char):
        if char in self.input_alphabet:
            idx = (self.output_alphabet.index(char) -
                   self.offset + self.ring_setting) % 26
            encrypted_char = self.input_alphabet[idx]
            return encrypted_char
        return char

    # Rotate the rotor by one position
    def rotate(self):
        self.offset = (self.offset + 1) % 26


# Reflector class represents the reflector in the Enigma machine
class Reflector:
    def __init__(self, wiring):
        # Input alphabet for the reflector
        self.input_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.output_alphabet = wiring  # The substitution wiring for the reflector

    # Reflects the input letter back using the reflector wiring
    def reflect(self, char):
        if char in self.input_alphabet:
            idx = self.input_alphabet.index(char)
            reflected_char = self.output_alphabet[idx]
            return reflected_char
        return char


# EnigmaMachine class represents the entire Enigma machine
class EnigmaMachine:
    def __init__(self, rotor_settings, reflector_wiring, plugboard_connections):
        self.rotors = []
        for i, (rotor_wiring, notch, ring_setting, offset) in enumerate(rotor_settings):
            self.rotors.append(
                Rotor(rotor_wiring, notch, ring_setting, offset))

        self.reflector = Reflector(reflector_wiring)

        self.plugboard_connections = plugboard_connections

    # Substitutes characters based on plugboard connections
    def substitute_plugboard(self, char):
        for plugboard_pair in self.plugboard_connections:
            if char == plugboard_pair[0]:
                return plugboard_pair[1]
            elif char == plugboard_pair[1]:
                return plugboard_pair[0]
        return char

    # Encrypts the message using the Enigma machine
    def encrypt(self, message):
        encrypted_message = ""
        for char in message.upper():
            char = self.substitute_plugboard(char)

            for rotor in self.rotors:
                char = rotor.substitute_forward(char)

            char = self.reflector.reflect(char)

            for rotor in reversed(self.rotors):
                char = rotor.substitute_backward(char)

            char = self.substitute_plugboard(char)

            encrypted_message += char

            # Rotate the first rotor, and if a notch is reached, rotate the next rotor
            self.rotors[0].rotate()
            for i in range(len(self.rotors) - 1):
                if self.rotors[i].offset == self.rotors[i].notch:
                    self.rotors[i + 1].rotate()

        return encrypted_message


def main():
    rotor_settings = [
        ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q", 0, 0),
        ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E", 0, 0),
        ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V", 0, 0),
    ]
    reflector_wiring = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
    plugboard_connections = [("A", "M"), ("G", "L"), ("P", "R"), ("S", "T")]

    enigma = EnigmaMachine(
        rotor_settings, reflector_wiring, plugboard_connections)
    message = "HELLO"
    encrypted_message = enigma.encrypt(message)
    print("Original message:", message)
    print("Encrypted message:", encrypted_message)


if __name__ == "__main__":
    main()
