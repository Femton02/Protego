import Handlebars from 'handlebars';

const handlebars = Handlebars.create();

export function bad(templateStr) {
  try {
    // expected vulnerability
    const template = handlebars.compile(templateStr, { noEscape: true });

    compiledTemplate = template(vars);
  } catch (err) {
    // ...
  }
}

export function ok(templateStr) {
  try {
    const template = handlebars.compile(templateStr, { noEscape: false });
    compiledTemplate = template(vars);
  } catch (err) {
    // ...
  }
}