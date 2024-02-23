# Internal Docs
This documentation provides technical details that are intended for internal developers only. 

## Table of Contents
- [Table of contents](#table-of-contents)
  * [Description](#description)
    - [Component Breakdown](#component-breakdown)
  * [Models](#models)
  * [Modules](#modules)

## Description
This document provides technical details that breakdown the core components of the Generative Personal Assistant along with specifications that scope out the current:
- feature-sets
- constraints/limitations

Each section concludes with a list of TODOs to motivate future work.  For additional information, technical diagrams depicting the prism portal are maintained [here](https://drive.google.com/drive/u/0/folders/1Cz6yqHKTaKw4BZlFSl1YuVwL1EMF6Xjv).

### Component Breakdown

The GPA is a monorepo built ontop of flask consisting on various modules that follow the [model-view-controller](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) software architecture.  With this paradigm in mind, the folder structure is represented as:

```bash
- app/ 
  - src/
      - module/   
        routes.py       # Controller
        - templates/    # View
    - model/            # Model
```

The next section will highlight key _entities_ (ie models) in the PrismPortal. This will lay the groundwork for defining the roles and reponsibilities of each _module_ (controllers).  The document will then conclude with _templates_: the front-end tooling used to render what is ultimately the user-experience.

### Models
A diagram depicting the relationship of data entities is provided [here](https://drive.google.com/file/d/14mUtcLdugNuaVt1Ronb7KJPRNRapfgLs/view?usp=drive_link).

### Modules
A system diagram depicting the relationship between modules is provided [here](https://drive.google.com/file/d/1lbwyHLE8VpgFxtbyxwCychiGsVB23kMb/view?usp=drive_link).

### Templates
