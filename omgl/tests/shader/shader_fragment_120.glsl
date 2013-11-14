#version 120

uniform sampler2D in_texture;

void main()
{
    gl_FragColor = texture2D(in_texture, gl_TexCoord[0].st);
}
