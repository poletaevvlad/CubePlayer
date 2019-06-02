#version 330 core

#define LIGHTS_COUNT 2

struct DirectionalLight{
    vec3 color;
    vec3 direction;
};


in vec3 trNormal;
in vec3 worldPos;
in vec2 texCoord;

out vec4 fragColor;
uniform DirectionalLight lights[LIGHTS_COUNT];
uniform sampler2D tex;

uniform vec3 colors[];


vec3 computeDuffuse(DirectionalLight light, vec3 normal){
    float diffuse = max(dot(normal, light.direction), 0.0);
    return diffuse * light.color;
}


vec3 computeSpecular(DirectionalLight light, vec3 normal, vec3 viewDirection,
                     float power){
    vec3 reflectDirection = reflect(-light.direction, normal);
    float specular = pow(max(dot(viewDirection, reflectDirection), 0.0), power);
    return specular * light.color;
}


vec3 blendColors(vec3 color1, vec3 color2, float alpha){
    return color2 * alpha + color1 * (1 - alpha);
}


void main(){
    vec3 normal = normalize(trNormal.xyz);
    vec3 viewDir = normalize(-worldPos);

    vec3 ambient = vec3(1.0, 1.0, 1.0) * 0.1;
    vec3 diffuse = vec3(0.0);
    vec3 specular = vec3(0.0);

    vec3 stickers_result = texture(tex, texCoord).rgb;
    float sticker_factor = stickers_result.r + stickers_result.g + stickers_result.b;

    float power = 6 + 10 * sticker_factor;
    for (int i = 0; i < LIGHTS_COUNT; i++){
        diffuse += computeDuffuse(lights[i], normal);
        specular += computeSpecular(lights[i], normal, viewDir, power);
    }

    vec3 materialColor = vec3(1.0, 1.0, 1.0);
    materialColor = blendColors(materialColor, colors[0], stickers_result.r);
    materialColor = blendColors(materialColor, colors[1], stickers_result.g);
    materialColor = blendColors(materialColor, colors[2], stickers_result.b);

    specular *= 0.4 + 0.6 * sticker_factor;

    fragColor = vec4(materialColor * (ambient + 0.9 * diffuse + 1.1 * specular), 1);
}