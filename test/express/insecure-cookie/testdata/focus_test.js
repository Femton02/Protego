var httpOnly;
{
	httpOnly: false
}

let x = false;

x = true;
{
	cookie: { httpOnly: x }
}