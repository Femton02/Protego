const { parse } = require('acorn');

function parseCode(code) {
    const ast = parse(code, { ecmaVersion: 2021 });
    return ast;
}

module.exports ={
    parseCode
};
