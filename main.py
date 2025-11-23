import tomllib
import yaml
import os
import re


def main():
    print("Hello from prj2env!")
    if os.path.exists("pyproject.toml") and os.path.exists("environment.yml"):
        with open("pyproject.toml", "rb") as f1:
            prjData = tomllib.load(f1)
        with open("environment.yml", "r") as f2:
            envData = yaml.safe_load(f2)
        d_prj = prjData.get("project", {})
        d_dep = d_prj.get("dependencies", [])
        print(f"need to transfer {d_dep}")
        env_d = envData.setdefault("dependencies", [])
        pip_e = [x for x in env_d if isinstance(x, str) and re.search(r"\b(pip)\b", x)]
        print(f"do i have pip? {pip_e}")
        if not pip_e:
            env_d.append("pip")
        pip_d = [x for x in env_d if isinstance(x, dict) and ("pip" in x)]
        print(f"do i have pip dict? {pip_d}")
        if len(pip_d) == 1:
            pip_list = pip_d[0].setdefault("pip", [])
        else:
            pip_list = []
            env_d.append({"pip": pip_list})
        pip_list.extend(d_dep)
        pip_list[:] = list(set(pip_list))
        env_d[:] = [x for x in env_d if isinstance(x, str)] + [
            x for x in env_d if isinstance(x, dict)
        ]
    else:
        if not os.path.exists("pyproject.toml"):
            print("pyproject.toml not found")
        if not os.path.exists("environment.yml"):
            print("environment.yml not found")
        return
    print(env_d)
    with open("environment.yml", "w") as f3:
        yaml.safe_dump(envData, f3, sort_keys=False)


if __name__ == "__main__":
    main()
