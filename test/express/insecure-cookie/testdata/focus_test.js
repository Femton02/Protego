var httpOnly;
{
	httpOnly = false
}

let x = false;

let y = x;
{
	cookie: {httpOnly: y }
}