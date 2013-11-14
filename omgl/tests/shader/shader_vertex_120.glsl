#version 120

attribute vec3 in_position;

void main()
{
    gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * vec4(in_position, 1.0);
    gl_FrontColor = gl_Color;
}
