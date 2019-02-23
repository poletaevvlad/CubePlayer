#version 330 core

in vec3 trNormal;
in vec3 worldPos;

out vec4 fragColor;


void main(){
    vec3 normal = normalize(trNormal.xyz);

    vec3 viewDir = normalize(/* 0 */ - worldPos);

    vec3 lightDir = normalize(vec3(1, 1, 1));

    float diffuse = max(dot(normal, lightDir), 0.0);

    vec3 reflectDir = reflect(-lightDir, normal);
    float specular = pow(max(dot(viewDir, reflectDir), 0.0), 2);

    vec3 ambientLight = vec3(1,1,1) * 0.1;
    vec3 diffuseLight = diffuse * vec3(1, 1, 1);
    vec3 specularLight = specular * vec3(1, 1, 0);

    fragColor = vec4(ambientLight + diffuseLight + specular, 1);
}