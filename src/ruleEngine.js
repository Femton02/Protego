const { parseCode } = require('./parser');
const rules = require('../rules/rules.json');

const sampleRules = rules.rules;

function analyzeCode(code) {
    const ast = parseCode(code);
    const matches = [];
    
    sampleRules.forEach(rule => {
        const regex = new RegExp(rule.pattern);
        const violations = findViolations(ast, regex);

        matches.push(...violations.map(violation => ({
            rule: rule.name,
            description: rule.description,
            location: getLocation(violation)
        })));
    });

    return matches;
}

function findViolations(node, regex) {
    let violations = [];
    
    if (node.type === "Program" || node.type === "BlockStatement") {
        node.body.forEach(childNode => {
            violations = violations.concat(findViolations(childNode, regex));
        });
    } else {
        Object.keys(node).forEach(key => {
            if (typeof node[key] === "object" && node[key] !== null) {
                violations = violations.concat(findViolations(node[key], regex));
            } else if (typeof node[key] === "string") {
                const matches = node[key].match(regex);
                if (matches) {
                    violations.push(node);
                }
            }
        });
    }
    
    return violations;
}

function getLocation(node) {
    return {
        start: node.start,
        end: node.end
    };
}

module.exports ={
    analyzeCode
};
