// ----------------------------------- Per Frame --------------------------------------
cbuffer UpdatePerFrame : register(b0)
{
	float4x4 viewI : ViewInverse < string UIWidget = "None"; >;

};

// --------------------------------------- Per Object -----------------------------------------
cbuffer UpdatePerObject : register(b1)
{
	float4x4 world : World < string UIWidget = "None"; >;

	int ClampDynamicLights
	<
		float UIMin = 0;
		float UISoftMin = 0;
		float UIMax = 99;
		float UISoftMax = 99;
		float UIStep = 1;
		string UIName = "ClampDynamicLights";
		string UIWidget = "Slider";
	> = 99;

	float4x4 wvp : WorldViewProjection < string UIWidget = "None"; >;

};

// --------------------------------------- Attributes -----------------------------------------
cbuffer UpdateAttributes : register(b2)
{
	float Val
	<
		float UIMin = 0.0;
		float UISoftMin = 0.0;
		float UIMax = 99.0;
		float UISoftMax = 99.0;
		float UIStep = 0.01;
		string UIName = "Val";
		string UIWidget = "Slider";
	> = 2.0;

};

// ----------------------------------- Lights --------------------------------------
cbuffer UpdateLights : register(b3)
{
	int Light0Type : LIGHTTYPE
	<
		string UIName =  "Light 0 Type";
		float UIMin = 0;
		float UIMax = 5;
		float UIStep = 1;
		string UIWidget = "None";
		string Object =  "Light 0";
	> = {3};

	int Light1Type : LIGHTTYPE
	<
		string UIName =  "Light 1 Type";
		float UIMin = 0;
		float UIMax = 5;
		float UIStep = 1;
		string UIWidget = "None";
		string Object =  "Light 1";
	> = {3};

	int Light2Type : LIGHTTYPE
	<
		string UIName =  "Light 2 Type";
		float UIMin = 0;
		float UIMax = 5;
		float UIStep = 1;
		string UIWidget = "None";
		string Object =  "Light 2";
	> = {3};

	float3 Light0Color : LIGHTCOLOR
	<
		string UIName =  "Light 0 Color";
		string UIWidget = "ColorPicker";
		string Object =  "Light 0";
	> = { 1.0, 1.0, 1.0};

	float3 Light1Color : LIGHTCOLOR
	<
		string UIName =  "Light 1 Color";
		string UIWidget = "ColorPicker";
		string Object =  "Light 1";
	> = { 1.0, 1.0, 1.0};

	float3 Light2Color : LIGHTCOLOR
	<
		string UIName =  "Light 2 Color";
		string UIWidget = "ColorPicker";
		string Object =  "Light 2";
	> = { 1.0, 1.0, 1.0};

	float Light0Intensity : LIGHTINTENSITY
	<
		string UIName =  "Light 0 Intensity";
		float UIMin = 0;
		float UIStep = 0.1;
		string Object =  "Light 0";
	> = 1.0;

	float Light1Intensity : LIGHTINTENSITY
	<
		string UIName =  "Light 1 Intensity";
		float UIMin = 0;
		float UIStep = 0.1;
		string Object =  "Light 1";
	> = 1.0;

	float Light2Intensity : LIGHTINTENSITY
	<
		string UIName =  "Light 2 Intensity";
		float UIMin = 0;
		float UIStep = 0.1;
		string Object =  "Light 2";
	> = 1.0;

	float3 Light0Pos : POSITION
	<
		string UIName =  "Light 0 Position";
		string Space = "World";
		string Object =  "Light 0";
	> = {1.0, 1.0, 1.0};

	float3 Light1Pos : POSITION
	<
		string UIName =  "Light 1 Position";
		string Space = "World";
		string Object =  "Light 1";
	> = {1.0, 1.0, 1.0};

	float3 Light2Pos : POSITION
	<
		string UIName =  "Light 2 Position";
		string Space = "World";
		string Object =  "Light 2";
	> = {1.0, 1.0, 1.0};

	float3 Light0Dir : DIRECTION
	<
		string UIName =  "Light 0 Direction";
		string Space = "World";
		string Object =  "Light 0";
	> = {0.0, -1.0, 0.0};

	float3 Light1Dir : DIRECTION
	<
		string UIName =  "Light 1 Direction";
		string Space = "World";
		string Object =  "Light 1";
	> = {0.0, -1.0, 0.0};

	float3 Light2Dir : DIRECTION
	<
		string UIName =  "Light 2 Direction";
		string Space = "World";
		string Object =  "Light 2";
	> = {0.0, -1.0, 0.0};

	float Light0Attenuation : DECAYRATE
	<
		string UIName =  "Light 0 Decay";
		float UIMin = 0;
		float UIStep = 1;
		string Object =  "Light 0";
	> = 0.0;

	float Light1Attenuation : DECAYRATE
	<
		string UIName =  "Light 1 Decay";
		float UIMin = 0;
		float UIStep = 1;
		string Object =  "Light 1";
	> = 0.0;

	float Light2Attenuation : DECAYRATE
	<
		string UIName =  "Light 2 Decay";
		float UIMin = 0;
		float UIStep = 1;
		string Object =  "Light 2";
	> = 0.0;

	float Light0ConeAngle : HOTSPOT
	<
		string UIName =  "Light 0 ConeAngle";
		float UIMin = 0;
		float UIMax = 1.571;
		float UIStep = 0.05;
		string Space = "World";
		string Object =  "Light 0";
	> = 0.46;

	float Light1ConeAngle : HOTSPOT
	<
		string UIName =  "Light 1 ConeAngle";
		float UIMin = 0;
		float UIMax = 1.571;
		float UIStep = 0.05;
		string Space = "World";
		string Object =  "Light 1";
	> = 0.46;

	float Light2ConeAngle : HOTSPOT
	<
		string UIName =  "Light 2 ConeAngle";
		float UIMin = 0;
		float UIMax = 1.571;
		float UIStep = 0.05;
		string Space = "World";
		string Object =  "Light 2";
	> = 0.46;

	float Light0Falloff : FALLOFF
	<
		string UIName =  "Light 0 Penumbra Angle";
		float UIMin = 0;
		float UIMax = 1.571;
		float UIStep = 0.05;
		string Object =  "Light 0";
	> = 0.7;

	float Light1Falloff : FALLOFF
	<
		string UIName =  "Light 1 Penumbra Angle";
		float UIMin = 0;
		float UIMax = 1.571;
		float UIStep = 0.05;
		string Object =  "Light 1";
	> = 0.7;

	float Light2Falloff : FALLOFF
	<
		string UIName =  "Light 2 Penumbra Angle";
		float UIMin = 0;
		float UIMax = 1.571;
		float UIStep = 0.05;
		string Object =  "Light 2";
	> = 0.7;

	bool Light0ShadowOn : SHADOWFLAG
	<
		string UIName =  "Light 0 Shadow";
		string Object =  "Light 0";
	> = true;

	bool Light1ShadowOn : SHADOWFLAG
	<
		string UIName =  "Light 1 Shadow";
		string Object =  "Light 1";
	> = true;

	bool Light2ShadowOn : SHADOWFLAG
	<
		string UIName =  "Light 2 Shadow";
		string Object =  "Light 2";
	> = true;

	float4x4 Light0ViewPrj : SHADOWMAPMATRIX
	<
		string Object =  "Light 0";
		string UIName =  "Light 0 Matrix";
		string UIWidget = "None";
	>;

	float4x4 Light1ViewPrj : SHADOWMAPMATRIX
	<
		string Object =  "Light 1";
		string UIName =  "Light 1 Matrix";
		string UIWidget = "None";
	>;

	float4x4 Light2ViewPrj : SHADOWMAPMATRIX
	<
		string Object =  "Light 2";
		string UIName =  "Light 2 Matrix";
		string UIWidget = "None";
	>;

	float3 Light0ShadowColor : SHADOWCOLOR
	<
		string UIName =  "Light 0 Shadow Color";
		string Object =  "Light 0";
	> = {0, 0, 0};

	float3 Light1ShadowColor : SHADOWCOLOR
	<
		string UIName =  "Light 1 Shadow Color";
		string Object =  "Light 1";
	> = {0, 0, 0};

	float3 Light2ShadowColor : SHADOWCOLOR
	<
		string UIName =  "Light 2 Shadow Color";
		string Object =  "Light 2";
	> = {0, 0, 0};

};

// ---------------------------------------- Textures -----------------------------------------
Texture2D Detail_D
<
	string ResourceName = "weld_ao.tif";
	string UIName = "Detail_D";
	string ResourceType = "2D";
	string UIWidget = "FilePicker";
>;

SamplerState MMMLWWWSampler
{
	Filter = MIN_MAG_MIP_LINEAR;
	AddressU = WRAP;
	AddressV = WRAP;
	AddressW = WRAP;
};

Texture2D Main_D
<
	string ResourceName = "badge_diff.tiff";
	string UIName = "Main_D";
	string ResourceType = "2D";
	string UIWidget = "FilePicker";
>;

Texture2D Main_N
<
	string ResourceName = "badge_norm.tif";
	string UIName = "Main_N";
	string ResourceType = "2D";
	string UIWidget = "FilePicker";
>;

Texture2D Detail_N
<
	string ResourceName = "weld_norm.tif";
	string UIName = "Detail_N";
	string ResourceType = "2D";
	string UIWidget = "FilePicker";
>;

Texture2D Light0ShadowMap : SHADOWMAP
<
	string ResourceName = "";
	string ResourceType = "2D";
	string UIWidget = "None";
	string Object =  "Light 0";
>;

Texture2D Light1ShadowMap : SHADOWMAP
<
	string ResourceName = "";
	string ResourceType = "2D";
	string UIWidget = "None";
	string Object =  "Light 1";
>;

Texture2D Light2ShadowMap : SHADOWMAP
<
	string ResourceName = "";
	string ResourceType = "2D";
	string UIWidget = "None";
	string Object =  "Light 2";
>;

SamplerState Light0ShadowMapSampler : SHADOWMAPSAMPLER
{
	Filter = MIN_MAG_MIP_POINT;
	AddressU = BORDER;
	AddressV = BORDER;
	AddressW = BORDER;
	BorderColor = float4(1.0,1.0,1.0,1.0);
};


// ---------------------------------------- Functions -----------------------------------------
int GetLightType(int ActiveLightIndex) 
{ 
	if (ActiveLightIndex == 0) 
		return Light0Type; 
	else if (ActiveLightIndex == 1) 
		return Light1Type; 
	else 
		return Light2Type; 
}

float3 GetLightColor(int ActiveLightIndex) 
{ 
	if (ActiveLightIndex == 0) 
		return Light0Color; 
	else if (ActiveLightIndex == 1) 
		return Light1Color; 
	else 
		return Light2Color; 
}

float GetLightIntensity(int ActiveLightIndex) 
{ 
	if (ActiveLightIndex == 0) 
		return Light0Intensity; 
	else if (ActiveLightIndex == 1) 
		return Light1Intensity; 
	else 
		return Light2Intensity; 
}

float3 GetLightPos(int ActiveLightIndex) 
{ 
	if (ActiveLightIndex == 0) 
		return Light0Pos; 
	else if (ActiveLightIndex == 1) 
		return Light1Pos; 
	else 
		return Light2Pos; 
}

float3 GetLightDir(int ActiveLightIndex) 
{ 
	if (ActiveLightIndex == 0) 
		return Light0Dir; 
	else if (ActiveLightIndex == 1) 
		return Light1Dir; 
	else 
		return Light2Dir; 
}

float GetLightAttenuation(int ActiveLightIndex) 
{ 
	if (ActiveLightIndex == 0) 
		return Light0Attenuation; 
	else if (ActiveLightIndex == 1) 
		return Light1Attenuation; 
	else 
		return Light2Attenuation; 
}

float GetLightConeAngle(int ActiveLightIndex) 
{ 
	if (ActiveLightIndex == 0) 
		return Light0ConeAngle; 
	else if (ActiveLightIndex == 1) 
		return Light1ConeAngle; 
	else 
		return Light2ConeAngle; 
}

float GetLightFalloff(int ActiveLightIndex) 
{ 
	if (ActiveLightIndex == 0) 
		return Light0Falloff; 
	else if (ActiveLightIndex == 1) 
		return Light1Falloff; 
	else 
		return Light2Falloff; 
}

bool GetLightShadowOn(int ActiveLightIndex) 
{ 
	if (ActiveLightIndex == 0) 
		return Light0ShadowOn; 
	else if (ActiveLightIndex == 1) 
		return Light1ShadowOn; 
	else 
		return Light2ShadowOn; 
}

float4x4 GetLightViewPrj(int ActiveLightIndex) 
{ 
	if (ActiveLightIndex == 0) 
		return Light0ViewPrj; 
	else if (ActiveLightIndex == 1) 
		return Light1ViewPrj; 
	else 
		return Light2ViewPrj; 
}

Texture2D GetLightShadowMap(int ActiveLightIndex) 
{ 
	if (ActiveLightIndex == 0) 
		return Light0ShadowMap; 
	else if (ActiveLightIndex == 1) 
		return Light1ShadowMap; 
	else 
		return Light2ShadowMap; 
}

float4 SampleFromShadowMap( int ActiveLightIndex, float2 UVs) 
{ 
	if (ActiveLightIndex == 0) 
		return Light0ShadowMap.SampleLevel(Light0ShadowMapSampler, UVs, 0); 
	else if (ActiveLightIndex == 1) 
		return Light1ShadowMap.SampleLevel(Light0ShadowMapSampler, UVs, 0); 
	else 
		return Light2ShadowMap.SampleLevel(Light0ShadowMapSampler, UVs, 0); 
}

float3 GetLightShadowColor(int ActiveLightIndex) 
{ 
	if (ActiveLightIndex == 0) 
		return Light0ShadowColor; 
	else if (ActiveLightIndex == 1) 
		return Light1ShadowColor; 
	else 
		return Light2ShadowColor; 
}


// -------------------------------------- APP and DATA  --------------------------------------
struct APPDATA
{
	float3 Position : POSITION;
	float2 map2 : TEXCOORD0;
	float2 map1 : TEXCOORD1;
	float3 Tangent : TANGENT;
	float3 Normal : NORMAL;
	float3 BiNormal : BINORMAL;
};

struct SHADERDATA
{
	float4 Position : SV_Position;
	float4 map2 : TEXCOORD0;
	float4 map1 : TEXCOORD1;
	float4 Tangent : TANGENT;
	float4 Normal : NORMAL;
	float4 WorldPosition : TEXCOORD2;
};

// -------------------------------------- CollapseRangeFunction --------------------------------------
struct CollapseRangeOutput
{
	float3 CollapsedVector;
};

CollapseRangeOutput CollapseRangeFunction(float3 Vector)
{
	CollapseRangeOutput OUT;

	float3 NormalMap = (Vector * 0.5);
	float3 AddOp = (NormalMap + 0.5);
	OUT.CollapsedVector = AddOp;

	return OUT;
}

// -------------------------------------- ReorientedNormalMappingFunction --------------------------------------
struct ReorientedNormalMappingOutput
{
	float3 Normal;
};

ReorientedNormalMappingOutput ReorientedNormalMappingFunction(float3 Base, float3 Detail)
{
	ReorientedNormalMappingOutput OUT;

	float3 MulOp = (float3(2.0, 2.0, 2.0) * Base);
	float3 VarT = (MulOp + float3(-1.0, -1.0, 0.0));
	float3 MulOp1379 = (Detail * float3(-2.0, -2.0, 2.0));
	float3 VarU = (MulOp1379 + float3(1.0, 1.0, -1.0));
	float3 MulOp1385 = (VarT * dot(VarT, VarU));
	float3 SubOp = ((MulOp1385 / VarT.z) - VarU);
	float3 NormOp = normalize(SubOp);
	CollapseRangeOutput CollapseRange1392 = CollapseRangeFunction(NormOp);
	OUT.Normal = CollapseRange1392.CollapsedVector;

	return OUT;
}

// -------------------------------------- ExpandRangeFunction --------------------------------------
struct ExpandRangeOutput
{
	float3 ExpandedVector;
};

ExpandRangeOutput ExpandRangeFunction(float3 Vector)
{
	ExpandRangeOutput OUT;

	float3 NormalMap = (Vector * 2.0);
	float3 NormalMap1479 = (NormalMap - 1.0);
	OUT.ExpandedVector = NormalMap1479;

	return OUT;
}

// -------------------------------------- TangentWorldConvertFunction --------------------------------------
struct TangentWorldConvertOutput
{
	float3 Vector;
};

TangentWorldConvertOutput TangentWorldConvertFunction(float TangentDirection, float3 Normal, float3 Tangent, float3 Vector)
{
	TangentWorldConvertOutput OUT;

	float3 Bn = (cross(Normal, Tangent) * TangentDirection);
	float3x3 toWorld = float3x3(Tangent, Bn, Normal);
	float3 TangentToWorld = mul(Vector, toWorld);
	OUT.Vector = TangentToWorld;

	return OUT;
}

// -------------------------------------- AmbientLightFunction --------------------------------------
struct AmbientLightOutput
{
	float3 LightColor;
};

AmbientLightOutput AmbientLightFunction(int ActiveLightIndex, float3 AlbedoColor, float3 LightColor, float LightIntensity)
{
	AmbientLightOutput OUT;

	float3 MulOp = (LightIntensity * (AlbedoColor * LightColor));
	OUT.LightColor = MulOp;

	return OUT;
}

// -------------------------------------- GetLightVectorFunction --------------------------------------
struct GetLightVectorOutput
{
	float3 Result;
};

GetLightVectorOutput GetLightVectorFunction(int ActiveLightIndex, float3 LightPosition, float3 VertexWorldPosition, int LightType, float3 LightDirection)
{
	GetLightVectorOutput OUT;

	bool IsDirectionalLight = (LightType == 4);
	float3 LerpOp = lerp((LightPosition - VertexWorldPosition), -(LightDirection), IsDirectionalLight);
	OUT.Result = LerpOp;

	return OUT;
}

// -------------------------------------- LambertDiffuseFunction --------------------------------------
struct LambertDiffuseOutput
{
	float3 Color;
};

LambertDiffuseOutput LambertDiffuseFunction(int ActiveLightIndex, float3 AlbedoColor, float3 Normal, float3 LightVector)
{
	LambertDiffuseOutput OUT;

	float SatOp = saturate(dot(Normal, LightVector));
	float3 Diffuse = (AlbedoColor * SatOp);
	OUT.Color = Diffuse;

	return OUT;
}

// -------------------------------------- LightDecayFunction --------------------------------------
struct LightDecayOutput
{
	float Attenuation;
};

LightDecayOutput LightDecayFunction(int ActiveLightIndex, float3 LightVectorUN, float Attenuation)
{
	LightDecayOutput OUT;

	bool IsAttenuationUsed = (Attenuation > 0.001);
	float DecayContribution482 = 0.0;
	if (IsAttenuationUsed)
	{
		float PowOp = pow(length(LightVectorUN), Attenuation);
		float DivOp = (1.0 / PowOp);
		DecayContribution482 = DivOp;
	}
	else
	{
		DecayContribution482 = 1.0;
	}
	OUT.Attenuation = DecayContribution482;

	return OUT;
}

// -------------------------------------- LightConeAngleFunction --------------------------------------
struct LightConeAngleOutput
{
	float ConeAngle;
};

LightConeAngleOutput LightConeAngleFunction(int ActiveLightIndex, float3 LightVector, float3 LightDirection, float ConeAngle, float ConeFalloff)
{
	LightConeAngleOutput OUT;

	float CosOp = cos(max(ConeFalloff, ConeAngle));
	float DotOp = dot(LightVector, -(LightDirection));
	float SmoothStepOp = smoothstep(CosOp, cos(ConeAngle), DotOp);
	OUT.ConeAngle = SmoothStepOp;

	return OUT;
}

// -------------------------------------- ShadowMapFunction --------------------------------------
struct ShadowMapOutput
{
	float LightGain;
};

ShadowMapOutput ShadowMapFunction(int ActiveLightIndex, float4x4 LightViewPrj, float ShadowMapBias, float3 VertexWorldPosition)
{
	ShadowMapOutput OUT;

	float IfElseOp564 = 0.0;
	float4 VectorConstruct = float4(VertexWorldPosition.x, VertexWorldPosition.y, VertexWorldPosition.z, 1.0);
	float4 MulOp = mul(VectorConstruct, LightViewPrj);
	float3 DivOp = (MulOp.xyz / MulOp.w);
	if (DivOp.x > -1.0 && DivOp.x < 1.0 && DivOp.y > -1.0 && DivOp.y < 1.0 && DivOp.z > 0.0 && DivOp.z < 1.0)
	{
		float Val552 = 0.5;
		float2 AddOp = ((DivOp.xy * Val552) + Val552);
		float SubOp = (DivOp.z - (ShadowMapBias / MulOp.w));
		float ShadowTotal = 0.0;
		for(int i=0; i<10; i+=1)
		{
			Texture2D _LightShadowMap = GetLightShadowMap(ActiveLightIndex);
			float2 MulOp604 = (float2(1.0, 1.0) * 0.00195313);
			float4 Sampler = SampleFromShadowMap(ActiveLightIndex, (float2(AddOp.x, 1.0-AddOp.y) + MulOp604));
			float IfElseOp558 = ((SubOp - Sampler.x) >= 0.0) ? (0.0) : (0.1);
			ShadowTotal += IfElseOp558;
		}
		IfElseOp564 = ShadowTotal;
	}
	else
	{
		IfElseOp564 = 1.0;
	}
	OUT.LightGain = IfElseOp564;

	return OUT;
}

// -------------------------------------- LightContributionFunction --------------------------------------
struct LightContributionOutput
{
	float3 Light;
};

LightContributionOutput LightContributionFunction(int ActiveLightIndex, float3 VertexWorldPosition, float3 LightVectorUN)
{
	LightContributionOutput OUT;

	float _LightIntensity = GetLightIntensity(ActiveLightIndex);
	int _LightType = GetLightType(ActiveLightIndex);
	bool IsDirectionalLight = (_LightType == 4);
	float DecayMul527 = 0.0;
	if (IsDirectionalLight)
	{
		DecayMul527 = 1.0;
	}
	else
	{
		float LightAttenuation = GetLightAttenuation(ActiveLightIndex);
		LightDecayOutput LightDecay476 = LightDecayFunction(ActiveLightIndex, LightVectorUN, LightAttenuation);
		DecayMul527 = LightDecay476.Attenuation;
	}
	bool IsSpotLight = (_LightType == 2);
	float ConeMul529 = 1.0;
	if (IsSpotLight)
	{
		float3 NormOp = normalize(LightVectorUN);
		float3 _LightDir = GetLightDir(ActiveLightIndex);
		float _LightConeAngle = GetLightConeAngle(ActiveLightIndex);
		float _LightFalloff = GetLightFalloff(ActiveLightIndex);
		LightConeAngleOutput LightConeAngle419 = LightConeAngleFunction(ActiveLightIndex, NormOp, _LightDir, _LightConeAngle, _LightFalloff);
		ConeMul529 = LightConeAngle419.ConeAngle;
	}
	bool _LightShadowOn = GetLightShadowOn(ActiveLightIndex);
	float ShadowMul530 = 1.0;
	if (_LightShadowOn)
	{
		float4x4 _LightViewPrj = GetLightViewPrj(ActiveLightIndex);
		ShadowMapOutput ShadowMap543 = ShadowMapFunction(ActiveLightIndex, _LightViewPrj, 0.01, VertexWorldPosition);
		float3 _LightShadowColor = GetLightShadowColor(ActiveLightIndex);
		float ShadowColorMix = lerp(ShadowMap543.LightGain, 1.0, _LightShadowColor.x);
		ShadowMul530 = ShadowColorMix;
	}
	float DecayShadowConeMul = (DecayMul527 * (ConeMul529 * ShadowMul530));
	float3 LightColor = GetLightColor(ActiveLightIndex);
	float3 MulItensity = (_LightIntensity * (DecayShadowConeMul * LightColor));
	OUT.Light = MulItensity;

	return OUT;
}

// -------------------------------------- BlinnSpecularFunction --------------------------------------
struct BlinnSpecularOutput
{
	float3 SpecularColor;
};

BlinnSpecularOutput BlinnSpecularFunction(int ActiveLightIndex, float3 LightVector, float3 Normal, float3 CameraVector, float SpecularPower, float3 SpecularColor)
{
	BlinnSpecularOutput OUT;

	float3 NormOp = normalize((LightVector + CameraVector));
	float SatOp = saturate(dot(Normal, NormOp));
	float3 BlinnSpec = (pow(SatOp, SpecularPower) * SpecularColor);
	float SatOp978 = saturate(dot(Normal, LightVector));
	float3 MulOp = (BlinnSpec * SatOp978);
	OUT.SpecularColor = MulOp;

	return OUT;
}

// -------------------------------------- DesaturateColorFunction --------------------------------------
struct DesaturateColorOutput
{
	float DesaturateColor;
};

DesaturateColorOutput DesaturateColorFunction(int ActiveLightIndex, float3 Color)
{
	DesaturateColorOutput OUT;

	float3 Col = float3(0.300008,0.6,0.100008);
	float DotOp = dot(saturate(Color), Col.xyz);
	OUT.DesaturateColor = DotOp;

	return OUT;
}

// -------------------------------------- DesaturateColorFunction --------------------------------------
DesaturateColorOutput DesaturateColorFunction(float3 Color)
{
	DesaturateColorOutput OUT;

	float3 Col = float3(0.300008,0.6,0.100008);
	float DotOp = dot(saturate(Color), Col.xyz);
	OUT.DesaturateColor = DotOp;

	return OUT;
}

// -------------------------------------- ShaderVertex --------------------------------------
SHADERDATA ShaderVertex(APPDATA IN)
{
	SHADERDATA OUT;

	OUT.Position = float4(IN.Position, 1);
	float4 OutUVs = float4(IN.map2.x, IN.map2.y, 0.0, 0.0);
	OUT.map2 = OutUVs;
	float4 OutUVs1249 = float4(IN.map1.x, IN.map1.y, 0.0, 0.0);
	OUT.map1 = OutUVs1249;
	float3 MulOp = mul(IN.Tangent, ((float3x3)world));
	float3 TangentNorm = normalize(MulOp);
	float4 WorldTangent = float4(TangentNorm.x, TangentNorm.y, TangentNorm.z, 1.0);
	OUT.Tangent = WorldTangent;
	float DotOp = dot(cross(IN.Normal, IN.Tangent), IN.BiNormal);
	float BiNormalDir1416 = (DotOp < 0.0) ? (-1.0) : (1.0);
	float4 VectorConstruct = float4(OUT.Tangent.xyz.x, OUT.Tangent.xyz.y, OUT.Tangent.xyz.z, BiNormalDir1416);
	OUT.Tangent = VectorConstruct;
	float3 MulOp1443 = mul(IN.Normal, ((float3x3)world));
	float3 NormalN = normalize(MulOp1443);
	float4 WorldNormal = float4(NormalN.x, NormalN.y, NormalN.z, 1.0);
	OUT.Normal = WorldNormal;
	float4 WorldPos = mul(OUT.Position, world);
	OUT.WorldPosition = WorldPos;
	float4 WVSpace = mul(OUT.Position, wvp);
	OUT.Position = WVSpace;

	return OUT;
}

// -------------------------------------- ShaderPixel --------------------------------------
struct PIXELDATA
{
	float4 Color : SV_Target;
};

PIXELDATA ShaderPixel(SHADERDATA IN, bool FrontFace : SV_IsFrontFace)
{
	PIXELDATA OUT;

	float InvertSatMask = (1.0 - saturate(0.0));
	float2 MulOp = (IN.map2.xy * Val);
	float4 Sampler = Detail_D.Sample(MMMLWWWSampler, float2(MulOp.x, 1-MulOp.y));
	float4 Sampler1258 = Main_D.Sample(MMMLWWWSampler, float2(IN.map1.xy.x, 1-IN.map1.xy.y));
	float3 MulOp1304 = (Sampler.xyz * Sampler1258.xyz);
	float3 ReplaceDiffuseWithReflection = (InvertSatMask * MulOp1304);
	float3 NormOp = normalize(IN.Normal.xyz);
	float3 NormOp1461 = normalize(IN.Tangent.xyz);
	float4 Sampler1607 = Main_N.Sample(MMMLWWWSampler, float2(IN.map1.xy.x, 1-IN.map1.xy.y));
	float4 Sampler1583 = Detail_N.Sample(MMMLWWWSampler, float2(MulOp.x, 1-MulOp.y));
	ReorientedNormalMappingOutput ReorientedNormalMapping1374 = ReorientedNormalMappingFunction(Sampler1607.xyz, Sampler1583.xyz);
	ExpandRangeOutput ExpandRange1475 = ExpandRangeFunction(ReorientedNormalMapping1374.Normal);
	float3 VectorConstruct = float3(1.0, 1.0, 1.0);
	float3 NormalMapH = (ExpandRange1475.ExpandedVector * VectorConstruct.xyz);
	TangentWorldConvertOutput TangentWorldConvert1462 = TangentWorldConvertFunction(IN.Tangent.w, NormOp, NormOp1461, NormalMapH);
	float3 TangentSpace = normalize(TangentWorldConvert1462.Vector);
	float3 FlippedNormals = lerp(-(TangentSpace), TangentSpace, FrontFace);
	float ClampOpacity = saturate(1.0);
	float3 CameraPosition = viewI[3].xyz;
	float3 CamVec = (CameraPosition - IN.WorldPosition.xyz);
	float3 CamVecNorm = normalize(CamVec);
	float4 LightLoopTotal11 = float4(0,0,0,0);
	for (int ActiveLightIndex = 0; ActiveLightIndex < 3; ++ActiveLightIndex)
	{
		if (ActiveLightIndex >= ClampDynamicLights) {continue;}
		int _LightType = GetLightType(ActiveLightIndex);
		bool IsAmbientLight = (_LightType == 5);
		float4 IfAmbientLight404 = float4(0, 0, 0, 0);
		if (IsAmbientLight)
		{
			float3 LightColor = GetLightColor(ActiveLightIndex);
			float _LightIntensity = GetLightIntensity(ActiveLightIndex);
			AmbientLightOutput AmbientLight409 = AmbientLightFunction(ActiveLightIndex, ReplaceDiffuseWithReflection, LightColor, _LightIntensity);
			float3 AmbientLightAndAO = (1.0 * AmbientLight409.LightColor);
			float4 VectorConstruct683 = float4(AmbientLightAndAO.x, AmbientLightAndAO.y, AmbientLightAndAO.z, 0.0);
			IfAmbientLight404 = VectorConstruct683;
		}
		else
		{
			float3 NoTranslucency = float3(0.0,0.0,0.0);
			float3 _LightPos = GetLightPos(ActiveLightIndex);
			float3 _LightDir = GetLightDir(ActiveLightIndex);
			GetLightVectorOutput GetLightVector851 = GetLightVectorFunction(ActiveLightIndex, _LightPos, IN.WorldPosition.xyz, _LightType, _LightDir);
			float3 LightVecNorm = normalize(GetLightVector851.Result);
			LambertDiffuseOutput LambertDiffuse827 = LambertDiffuseFunction(ActiveLightIndex, ReplaceDiffuseWithReflection, FlippedNormals, LightVecNorm);
			LightContributionOutput LightContribution417 = LightContributionFunction(ActiveLightIndex, IN.WorldPosition.xyz, GetLightVector851.Result);
			float3 AddTranslucency = (NoTranslucency.xyz + (LambertDiffuse827.Color * LightContribution417.Light));
			float3 Col = float3(1.0,1.0,1.0);
			BlinnSpecularOutput BlinnSpecular966 = BlinnSpecularFunction(ActiveLightIndex, LightVecNorm, FlippedNormals, CamVecNorm, 20.0, Col.xyz);
			float3 SpecLightIntensity = (LightContribution417.Light * BlinnSpecular966.SpecularColor);
			float3 Diffuse_Spec = ((AddTranslucency * ClampOpacity) + SpecLightIntensity);
			DesaturateColorOutput DesaturateColor675 = DesaturateColorFunction(ActiveLightIndex, SpecLightIntensity);
			float4 Color_Alpha = float4(Diffuse_Spec.x, Diffuse_Spec.y, Diffuse_Spec.z, DesaturateColor675.DesaturateColor);
			IfAmbientLight404 = Color_Alpha;
		}
		float4 ApplyWeight415 = IfAmbientLight404;
		LightLoopTotal11 += ApplyWeight415;
	}
	float3 NoReflection = float3(0.0,0.0,0.0);
	float3 ReflectXmask = (0.0 * NoReflection.xyz);
	float3 DefaultEmissiveColor = float3(0.0,0.0,0.0);
	float3 DefaultIBLColor = float3(0.0,0.0,0.0);
	float3 PreMultipliedAlpha = ((DefaultEmissiveColor.xyz + DefaultIBLColor.xyz) * ClampOpacity);
	float3 AddReflection = (ReflectXmask + PreMultipliedAlpha);
	DesaturateColorOutput DesaturateColor384 = DesaturateColorFunction(ReflectXmask);
	float OpacityAndReflection = (ClampOpacity + DesaturateColor384.DesaturateColor);
	float4 TotalAmbientAndOpacity = float4(AddReflection.x, AddReflection.y, AddReflection.z, OpacityAndReflection);
	float4 LightLoopAndAfterLoop = (LightLoopTotal11 + TotalAmbientAndOpacity);
	float SatOp = saturate(LightLoopAndAfterLoop.w);
	float4 VectorConstruct31 = float4(LightLoopAndAfterLoop.xyz.x, LightLoopAndAfterLoop.xyz.y, LightLoopAndAfterLoop.xyz.z, SatOp);
	OUT.Color = VectorConstruct31;

	return OUT;
}

// -------------------------------------- technique T0 ---------------------------------------
technique11 T0
<
	bool overridesDrawState = false;
	int isTransparent = 0;
>
{
	pass P0
	<
		string drawContext = "colorPass";
	>
	{
		SetVertexShader(CompileShader(vs_5_0, ShaderVertex()));
		SetPixelShader(CompileShader(ps_5_0, ShaderPixel()));
		SetHullShader(NULL);
		SetDomainShader(NULL);
		SetGeometryShader(NULL);
	}

}

