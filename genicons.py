#!/usr/bin/env python3

import os
import re


def all_puml_files_iterator(root_dir):
    return (
        os.path.join(dp, f)
        for dp, dn, filenames in os.walk(root_dir)
        for f in filenames
        if os.path.splitext(f)[1] == ".puml"
    )


def get_folder_and_name(puml_file_path):
    relpath = os.path.relpath(puml_file_path)
    return os.path.dirname(relpath), os.path.splitext(os.path.basename(relpath))[0]


paths_and_names = map(get_folder_and_name, all_puml_files_iterator("."))

items_dict = {}
for path, name in paths_and_names:
    items_dict[path] = items_dict.get(path, []) + [name]
items_dict.pop("")

print(
    """
<html>
  <head>
    <title>Plantuml Icon Font Sprites Overview</title>
    <style>
    .cards {
      display: flex;
      flex-wrap: wrap;
      align-items: stretch;
    }
    .card {
      flex: 0 0 200px;
      margin: 10px;
      border: 1px solid #ccc;
      box-shadow: 2px 2px 6px 0px  rgba(0,0,0,0.3);
    }
    .card img {
      max-width: 100%;
      margin-left: auto;
      margin-right: auto;
      display: block;
      padding-top: 10px;
    }
    .card .text {
      padding: 0 20px 10px;
    }
    pre {
      font-size: small;
    }
    </style>
  </head>
  <body>
"""
)

for folder, names in items_dict.items():
    print(
        f"""
    <h1>Folder "{folder}"</h1>
    <main class="cards">
"""
    )
    for name in names:
        with open(folder+"/"+name+".puml", 'r') as searchfile:
            for line in searchfile:
                r=re.search('.*!define (.*?)\((.*)',line)
                macro=""
                if r:
                    macro = r.group(1)
                    break

        print(
            f"""
      <article class="card">
        <img src="{folder}/{name}.png">
        <div class="text">
          <h2>{name}</h2>
          <pre>
!include common.puml
!include {folder}/{name}.puml
"""+ macro +
"""
</pre>
        </div>
      </article>
"""
        )

    print(
        """
    </main>
    <hr/>
"""
    )

print(
    """
  </body>
</html>
"""
)
