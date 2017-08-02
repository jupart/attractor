---VERTEX SHADER---
#ifdef GL_ES
    precision highp float;
#endif

/* INPUTS - vertex attributes */
attribute vec2 pos;
attribute vec2 uvs;

/* OUTPUTS - to the fragment shader */
varying vec4 frag_color;
varying vec2 tex_coord0;

/* uniform variables */
uniform mat4 modelview_mat;
uniform mat4 projection_mat;
uniform vec4 color;
uniform float opacity;

void main(void) {
	frag_color = color * vec4(1., 1., 1., opacity);
	tex_coord0 = uvs;
	vec4 new_pos = vec4(pos.xy, 0., 1.);

	// Special keyword - gl_Position
	gl_Position = projection_mat * modelview_mat * new_pos;

}


---FRAGMENT SHADER---
#ifdef GL_ES
	precision highp float;
#endif

/* INPUTS - from the vertex shader */
varying vec4 frag_color;
varying vec2 tex_coord0;

/* uniform texture samplers */
uniform sampler2D texture0;

void main(void) {
	// Special keyword - gl_Position
	gl_FragColor = frag_color * texture2D(texture0, tex_coord0);
}
