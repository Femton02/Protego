const fs = require('fs');
const { parseCode } = require('./parser');
const walk = require('acorn-walk');

// Load rules from rules.json
const rules = JSON.parse(fs.readFileSync('../rules/rules.json', 'utf8')).rules;

function analyzeCodeWithLines(code) {
    const ast = parseCode(code);

    const vulnerabilities = [];

    // Traverse the AST
    walk.simple(ast, {
        Literal(node) {
            // Check if the node matches any rule pattern
            for (const rule of rules) {         
            const regex = new RegExp(rule.pattern);
            if (regex.test(node.raw)) {
                // Report vulnerability
                vulnerabilities.push({
                ruleName: rule.name,
                description: rule.description,
                location: {
                    start: node.start,
                    end: node.end,
                },
                line: code.substring(node.start, node.end)
                });
                break;
            }
            }
        },
    });

    return vulnerabilities;
}

module.exports = {
    analyzeCodeWithLines,
};
