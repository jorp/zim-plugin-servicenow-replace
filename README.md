# zim-plugin-servicenow-replace
Zim plugin to replace ServiceNow regexes with a link.

## Overview

Add text to project:

```
INC4353455
```

Press `<ENTER>` or `<SPACE>` and voilà:

```
[[https://SERVICENOW_DOMAIN/incident.do?sysparm_query=number=INC4353455|INC4353455]]
```

the text is replaced automatically by a handler.

### (Potential) TODO
* GUI configuration from within the plugin menu
* Extensibility beyond ServiceNow
