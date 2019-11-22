from dataclasses import dataclass


@dataclass
class Argument:
    name: str
    description: str
    short: str = None
    required: bool = False
    value: str = None

    def description_string(self, named: bool) -> str:
        short_string = f"/-{self.short}" if self.short is not None and named else ""
        optional_string = " (optional)" if not self.required else ""
        name_string = f"--{self.name}" if named else self.name
        return f"{name_string}{short_string}\t{self.description}{optional_string}"
