uniform texture2d uv_map;

sampler_state PointSampler
{
	Filter = Point;
	AddressU = Clamp;
	AddressV = Clamp;

};

float4 mainImage(VertData v_in) : TARGET
{
	float4 uv_data = uv_map.Sample(PointSampler, v_in.uv);
	float2 uv;
	uv.x = uv_data.r + uv_data.g / 255;
	uv.y = uv_data.b + uv_data.a / 255;
	float4 ret = image.Sample(PointSampler, uv);
	return ret;
}