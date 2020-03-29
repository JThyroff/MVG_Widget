//Fragment Shader

#ifdef GL_ES
precision highp float;
#endif

/* Outputs from the vertex shader */
varying vec4 frag_color;
varying vec2 tex_coord0;

/* uniform texture samplers */
//uniform sampler2D texture0;

uniform float t;//time
uniform sampler2D tex_in;
uniform sampler2D tex_out;

/* custom one */
uniform vec2 resolution;
//uniform float time;

void main (void){
    //gl_FragColor = frag_color * texture2D(texture0, tex_coord0);
    vec4 cin = texture2D(tex_in, tex_coord0);
    vec4 cout = texture2D(tex_out, tex_coord0);
    gl_FragColor = mix(cout, cin, t);
}