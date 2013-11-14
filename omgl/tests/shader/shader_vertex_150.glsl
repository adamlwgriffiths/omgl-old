#version 150

in mat4 in_projection;
in mat4 in_model_view;
in vec3 in_position;

void main()
{
    gl_Position = in_projection * in_model_view * vec4(in_position, 1.0);
    gl_FrontColor = gl_Color;
}
