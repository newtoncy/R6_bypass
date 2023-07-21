uniform texture2d other_image;
uniform float alpha = 0.75;

float4 mainImage(VertData v_in) : TARGET
{
	float4 other = other_image.Sample(textureSampler, v_in.uv);
	float4 base = image.Sample(textureSampler, v_in.uv);
	float3 ret = (base - alpha * other) / (1-alpha);
	return float4(ret, 1);
}
