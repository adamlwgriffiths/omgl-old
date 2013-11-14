#version 150

in vec2 in_texture_coord;
uniform sampler2D in_texture;
out vec3 out_frag;

void main()
{
    out_frag = texture2D(in_texture, in_texture_coord.st);
}
