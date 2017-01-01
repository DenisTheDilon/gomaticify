# Gomaticify - YAML to Gomatic

This is a Python helper that convert a [YAML](http://yaml.org/) file or string to our beautiful and poorly documented [Gomatic](https://github.com/SpringerSBM/gomatic).

## The YAML file...

...look like this:

```yaml
pipeline-groups:
- group: string1234
  authorization:
    view:
      users:
      - string1234
      roles:
      - string1234
    operate:
      users:
      - string1234
      roles:
      - string1234
    admins:
      users:
      - string1234
      roles:
      - string1234
  pipelines:
  - name: string1234
    is-locked: false
    label-template: string1234
    template: string1234
    params:
    - name: string1234
      value: string1234
    #tracking-tool: 
    #  link: str1234
    #  regex: str1234
    timer:
      only-on-changes: true
      value: str1234
    environment-variables:
    - name: string1234
      secure: true
      encrypted-value: string1234
    - name: str1234
      value: str1234
    #dependencies:
    #- pipeline: str1234
    #  stage: str1234
    materials:
      git:
      - material-name: string1234
        url: url
        branch: string1234
        auto-update: true
        dest: /path
        #shallow-clone: true
        #invert-filter: true
        filter-ignore-patterns: 
        - 'string1234'
      package:
      - ref: string1234
      pipeline:
      - material-name: string1234
        pipeline-name: string1234
        stage-name: string1234
      #svn:
      #- url: string1234
      #  username: string1234
      #  password: string1234
      #  encrypted-password: string1234
      #  check-externals: true
      #  dest: /path
      #  material-name: string1234
      #  auto-update: true
      #  invert-filter: true
      #  filter-ignore-patterns: 
      #  - 'string1234'
      #hg:
      #- url: string1234
      #  dest: /path
      #  material-name: string1234
      #  auto-update: true
      #  invert-filter: true
      #  filter-ignore-patterns: 
      #  - 'string1234'
      #p4:
      #- port: string1234
      #  username: string1234
      #  password: string1234
      #  encrypted-password: string1234
      #  use-tickets: true
      #  dest: /path
      #  material-name: string1234
      #  auto-update: true
      #  invert-filter: true
      #  ?view: a
      #  filter-ignore-patterns: 
      #  - 'string1234'
      #tfs:
      #- url: string1234
      #  username: string1234
      #  domain: string1234
      #  password: string1234
      #  encrypted-password: string1234
      #  project-path: string1234
      #  dest: /path
      #  material-name: string1234
      #  auto-update: true
      #  invert-filter: true
      #  filter-ignore-patterns: 
      #  - 'string1234'
      #scm:
      #- ref: string1234
      #  dest: /path
      #  filter-ignore-patterns: 
      #  - 'string1234'
    stages:
    - name: string1234
      clean-working-dir: true
      fetch-materials: false
      #artifact-cleanup-prohibited: true    
      approval:
        type: manual
        authorization:
          users:
          - string1234
          roles:
          - string1234
      environment-variables:
      - name: string1234
        secure: true
        encrypted-value: string1234
      - name: string1234
        value: string1234
      jobs:
      - name: string1234
        run-on-all-agents: true
        #run-instance-count: 745 
        timeout: 3.14
        #elastic-profile-id: string1234        
        environment-variables:
        - name: string1234
          value: string1234
        - name: string1234
          secure: true
          encrypted-value: string1234
        tasks:
          #task:
          #- description: description
          #  plugin-configuration:
          #    id: string1234
          #    version: string1234
          #  configuration:
          #  - key: string1234
          #    value: string1234
          #  - key: string1234
          #    encryptedValue: string1234
          #  runif: passed
          #  on-cancel:
          #ant:
          #- target: /path
          #  working-dir: string1234
          #  build-file: string1234
          #  runif: passed
          #  on-cancel:
          #nant:
          #- nant-path: string1234
          #  target: /path
          #  working-dir: string1234
          #  build-file: string1234
          #  runif: passed
          #  on-cancel:
          exec:
          - command: string1234
            args: 
            - 'string1234'
            working-dir: /path
            #timeout: 100
            runif: passed
            #on-cancel:
          rake:
          - target: /path
            #working-dir: string1234
            #build-file: string1234
            runif: passed
            #on-cancel:          
          fetch-artifact:
          - pipeline: string1234
            stage: string1234
            job: string1234
            src: /path
            dest: /path
            runif: passed
            #target: /path
            #working-dir: string1234
            #build-file: string1234          
            #on-cancel:     
        #artifacts:
        #- src: string1234
        #- dest: /path
        resources:
        - 'string1234'
        tabs:
        - name: string1234
          path: reports/report.html
        #properties:
        #- name: string1234
        #  src: string1234
        #  xpath: string1234
templates:
- name: string1234
  authorization:
    roles:
    - string1234
    users:
    - string1234
  stages:
  - name: string1234
    clean-working-dir: true
    fetch-materials: false
    #artifact-cleanup-prohibited: true    
    approval:
      type: manual
      authorization:
        users:
        - string1234
        roles:
        - string1234
    environment-variables:
    - name: string1234
      secure: true
      encrypted-value: string1234
    - name: string1234
      value: string1234
    jobs:
    - name: string1234
      run-on-all-agents: true
      #run-instance-count: 745 
      timeout: 3.14
      #elastic-profile-id: string1234        
      environment-variables:
      - name: string1234
        value: string1234
      - name: string1234
        secure: true
        encrypted-value: string1234
      tasks:
        #task:
        #- description: description
        #  plugin-configuration:
        #    id: string1234
        #    version: string1234
        #  configuration:
        #  - key: string1234
        #    value: string1234
        #  - key: string1234
        #    encryptedValue: string1234
        #  runif: passed
        #  on-cancel:
        #ant:
        #- target: /path
        #  working-dir: string1234
        #  build-file: string1234
        #  runif: passed
        #  on-cancel:
        #nant:
        #- nant-path: string1234
        #  target: /path
        #  working-dir: string1234
        #  build-file: string1234
        #  runif: passed
        #  on-cancel:
        exec:
        - command: string1234
          args: 
          - 'string1234'
          working-dir: /path
          #timeout: 100
          runif: passed
          #on-cancel:
        rake:
        - target: /path
          #working-dir: string1234
          #build-file: string1234
          runif: passed
          #on-cancel:          
        fetch-artifact:
        - pipeline: string1234
          stage: string1234
          job: string1234
          src: /path
          dest: /path
          runif: passed
          #target: /path
          #working-dir: string1234
          #build-file: string1234          
          #on-cancel:     
      #artifacts:
      #- src: string1234
      #- dest: /path
      resources:
      - 'string1234'
      tabs:
      - name: string1234
        path: reports/report.html
      #properties:
      #- name: string1234
      #  src: string1234
      #  xpath: string1234
```

### Some important details

The current version of Gomatic don't support the `package material`, the `authorization` tag and HTTPS/Aunthenticated GoCD server, for those cases you can use this [fork](https://github.com/DenisTheDilon/gomatic).

## Usage

Just do it for YAML string...

```python
from gomaticify import YamlToGomaticConverter

converter = YamlToGomaticConverter(your_host, username=your_username, password=your_password, ssl=False, verify_ssl=True)
go_cd_configurator = converter.convert_from_yaml_string(your_yaml_formatted_string)
```

... and for YAML file.

```python
from gomaticify import YamlToGomaticConverter

converter = YamlToGomaticConverter(your_host, username=your_username, password=your_password, ssl=False, verify_ssl=True)
go_cd_configurator = converter.convert_from_yaml_file(path_for_your_yaml)
```

You also have the option to execute Gomaticify and Gomatic from CLI like this..

```
python -m gomaticify --server="10.12.12.12" --username="user" --password="pass" --ssl=False --verify_ssl=False --yaml_path="/drives/repo/gocd.yml" --save_locally=True
```

## Known Issues

Only God knows...
I created this to a specific need, so probably the YAML doesn't attend many GoCD structures.
Gomaticify will always ensure/recreate things, so be careful with your pipeline groups and templates