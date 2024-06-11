// expected vulnerability
const sanitizedUserInput = user.Input.replaceAll('<', '&lt;').replaceAll('>', '&gt;');
const html = `<strong>${sanitizedUserInput}</strong>`;

user.Input.replaceAll(a, 'other');