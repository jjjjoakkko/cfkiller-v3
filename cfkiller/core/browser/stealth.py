# cfkiller/core/browser/stealth.py
# Descargar de: https://raw.githubusercontent.com/berstend/puppeteer-extra/master/packages/puppeteer-extra-plugin-stealth/evasions/index.js
# Guardar como stealth.min.js en la raíz o en cfkiller/core/browser/

STEALTH_SCRIPT = """
// stealth.min.js contenido completo (o carga desde archivo)
const fs = require('fs');
module.exports = function() {
  // evasions: navigator.webdriver, chrome.runtime, plugins, languages, etc.
  delete navigator.__proto__.webdriver;
  // ... (el script completo de 300 líneas)
};
"""

# O más simple: solo indicamos que existe
STEALTH_PLUGIN_PATH = "cfkiller/core/browser/stealth.min.js"

# En manager.py usarás:
# await context.add_init_script(path=STEALTH_PLUGIN_PATH)