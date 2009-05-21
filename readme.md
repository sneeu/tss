Tumble Style Sheets ("TSS")
===========================

This is a first stab at a parser for what might me a nice addition to CSS. I'm pretty happy with the W3C's CSS, and this is only really the expansion of an idea. Not all selectors are implemented, but tag names, classes, and IDs should work.

I was thinking about Jeff Croft's contentious blog post [Applying OOP Concepts CSS][jeffcroftcss], and what CSS would look like if it were a little more OO. This is what came out:

	abstract .box {
		border: 1px solid;
		color: #222
	}

	.message (.box){
		width: 100%;
	}

	.error (.message){
		background: #fcc;
		color: #c00;
	}

The additions are the `abstract` keyword (which prevents classes from being output), and the extends pattern, which is the parenthesis (`()`) above.

The output of this "TSS" would be:

	.message {
		color: #222;
		width: 100%;
		border: 1px solid;
	}
	.error {
		color: #c00;
		width: 100%;
		border: 1px solid;
		background: #fcc;
	}

[jeffcroftcss]: http://jeffcroft.com/blog/2009/may/20/applying-oop-concepts-css/
