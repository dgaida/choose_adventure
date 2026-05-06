const fs = require('fs');
const content = fs.readFileSync('src/templates/story_template.html', 'utf8');
if (content.includes('const words = Object.keys(vocabData).sort((a, b) => b.length - a.length);')) {
    console.log('Single-pass regex found');
} else {
    console.log('Old regex logic found');
    process.exit(1);
}
