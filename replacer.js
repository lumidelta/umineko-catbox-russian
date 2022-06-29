const fs = require('fs')
let targetScript = fs.readFileSync('script_replace.rb', 'utf-8')
const scriptBase = `${process.argv[2]}`
const scriptJp = `${scriptBase}_extracted.rb`
const scriptEn = `${scriptBase}.txt`
// if (!fs.existsSync(scriptJp) || !fs.existsSync(scriptEn)) process.exit()

const linesJp = fs.readFileSync(scriptJp, 'utf-8').split('\n')
const linesEn = fs.readFileSync(scriptEn, 'utf-8').split('\n')
const replaceDialogue = true
const lineFuns = replaceDialogue ? [x => x + '@', x => x + "'", x => x.trim() + '@', x => x.trim() + "'"] : [x => x, x => x.trim()]
for (let i = 0; i < linesJp.length; i++) {
  if (linesEn[i]) {
    for (const fun of lineFuns) {
      const tmpScript = targetScript.replace(fun(linesJp[i]), fun(linesEn[i]))
      if (tmpScript !== targetScript) {
        targetScript = tmpScript
        break
      }
    }
  }
  // linesEn[i] = linesEn[i].split("\"").join("")
  // linesJp[i] = linesJp[i].split("\"").join("")
  // const replaceDialogue2 = false
  // const lineFuns2 = replaceDialogue2 ? [x => x + '@', x => x + "'", x => x.trim() + '@', x => x.trim() + "'"] : [x => x, x => x.trim()]
  // if (linesEn[i]) {
  //   for (const fun of lineFuns2) {
  //     const tmpScript = targetScript.replace(fun(linesJp[i]), fun(linesEn[i]))
  //     if (tmpScript !== targetScript) {
  //       targetScript = tmpScript
  //       break
  //     }
  //   }
  // }
}
fs.writeFileSync('script_replace.rb', targetScript, 'utf-8')
