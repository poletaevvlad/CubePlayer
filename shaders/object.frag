#version 330 core

#define LIGHTS_COUNT 2

const float PI_2 = 1.57079632679489661923;

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
uniform sampler2D labels_tex;
uniform sampler2D label;

uniform float label_rotation;
uniform vec3 label_color_visibility;
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


vec2 getLabelUV(vec3 label_data){
    float angle = abs(label_rotation) * PI_2;
    float s = sin(angle), c = cos(angle);
    vec2 uv = vec2(label_data.x * c - label_data.y * s,
                   label_data.x * s + label_data.y * c);
    if (label_rotation < 0){
        uv.x = 1 - uv.x;
    }
    return uv;
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

    vec3 material_color = vec3(1.0, 1.0, 1.0);
    material_color = blendColors(material_color, colors[0], stickers_result.r);
    material_color = blendColors(material_color, colors[1], stickers_result.g);
    material_color = blendColors(material_color, colors[2], stickers_result.b);

    float label_visibility = label_color_visibility.r * stickers_result.r + \
                             label_color_visibility.g * stickers_result.g + \
                             label_color_visibility.b * stickers_result.b;
    vec3 label_data = texture(labels_tex, texCoord).rgb;
    vec4 label_color = texture(label, getLabelUV(label_data));
    float label_transparency = label_color.a * label_visibility * label_data.b;

    material_color = blendColors(material_color, label_color.rgb, label_transparency);

    specular *= 0.4 + 0.6 * sticker_factor;

    fragColor = vec4(material_color * (ambient + 0.9 * diffuse + 1.1 * specular), 1);
}