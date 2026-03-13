import os
import re

files_to_process = [
    r"src\main\java\com\accisense\model\Accident.java",
    r"src\main\java\com\accisense\model\RoadSegment.java",
    r"src\main\java\com\accisense\model\UserLocation.java",
    r"src\main\java\com\accisense\dto\AlertDTO.java",
    r"src\main\java\com\accisense\dto\LocationDTO.java"
]

for filepath in files_to_process:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove lombok imports and annotations
    content = re.sub(r'import\s+lombok\.[a-zA-Z0-9_]+;\n*', '', content)
    content = re.sub(r'@Data\n', '', content)
    content = re.sub(r'@Getter\n', '', content)
    content = re.sub(r'@Setter\n', '', content)
    content = re.sub(r'@NoArgsConstructor\n', '', content)
    content = re.sub(r'@AllArgsConstructor\n', '', content)
    content = re.sub(r'@Builder\n', '', content)

    # find all private fields
    # e.g., private String name;
    # or private Double latitude;
    fields = re.findall(r'private\s+([a-zA-Z0-9_\<\>]+)\s+([a-zA-Z0-9_]+)\s*(?:=[^;]+)?;', content)

    methods = []
    for type_name, var_name in fields:
        capitalized = var_name[0].upper() + var_name[1:]
        
        # getter
        getter = f"    public {type_name} get{capitalized}() {{\n        return {var_name};\n    }}"
        methods.append(getter)
        
        # setter
        setter = f"    public void set{capitalized}({type_name} {var_name}) {{\n        this.{var_name} = {var_name};\n    }}"
        methods.append(setter)
    
    if methods:
        methods_str = "\n\n" + "\n\n".join(methods) + "\n"
        
        # insert before the last closing brace
        last_brace_idx = content.rfind('}')
        if last_brace_idx != -1:
            new_content = content[:last_brace_idx] + methods_str + content[last_brace_idx:]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Processed {filepath}")
        else:
            print(f"Failed to find closing brace in {filepath}")
