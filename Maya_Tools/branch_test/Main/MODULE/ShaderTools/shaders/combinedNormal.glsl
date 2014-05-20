#version 400
// ----------------------------------------- Header ------------------------------------------
#define float2 vec2
#define float3 vec3
#define float4 vec4
#define float3x3 mat3
#define float4x4 mat4
#ifdef COMPILING_VS
	#define OUTIN out 
#else 
	#define OUTIN in 
#endif 



// ----------------------------------- Per Frame --------------------------------------
uniform float4x4 viewI;


// --------------------------------------- Per Object -----------------------------------------
uniform float4x4 world;

uniform int ClampDynamicLights = 99;

uniform float4x4 wvp;


// --------------------------------------- Attributes -----------------------------------------
uniform float Val = 2.0;


// ----------------------------------- Lights --------------------------------------
uniform int Light0Type = 3;

uniform int Light1Type = 3;

uniform int Light2Type = 3;

uniform float3 Light0Color = float3( 1.0, 1.0, 1.0 );

uniform float3 Light1Color = float3( 1.0, 1.0, 1.0 );

uniform float3 Light2Color = float3( 1.0, 1.0, 1.0 );

uniform float Light0Intensity = 1.0;

uniform float Light1Intensity = 1.0;

uniform float Light2Intensity = 1.0;

uniform float3 Light0Pos = float3(1.0, 1.0, 1.0);

uniform float3 Light1Pos = float3(1.0, 1.0, 1.0);

uniform float3 Light2Pos = float3(1.0, 1.0, 1.0);

uniform float3 Light0Dir = float3(0.0, -1.0, 0.0);

uniform float3 Light1Dir = float3(0.0, -1.0, 0.0);

uniform float3 Light2Dir = float3(0.0, -1.0, 0.0);

uniform float Light0Attenuation = 0.0;

uniform float Light1Attenuation = 0.0;

uniform float Light2Attenuation = 0.0;

uniform float Light0ConeAngle = 0.46;

uniform float Light1ConeAngle = 0.46;

uniform float Light2ConeAngle = 0.46;

uniform float Light0Falloff = 0.7;

uniform float Light1Falloff = 0.7;

uniform float Light2Falloff = 0.7;

uniform bool Light0ShadowOn = true;

uniform bool Light1ShadowOn = true;

uniform bool Light2ShadowOn = true;

uniform float4x4 Light0ViewPrj;

uniform float4x4 Light1ViewPrj;

uniform float4x4 Light2ViewPrj;

uniform float3 Light0ShadowColor = float3(0, 0, 0);

uniform float3 Light1ShadowColor = float3(0, 0, 0);

uniform float3 Light2ShadowColor = float3(0, 0, 0);


// ---------------------------------------- Textures -----------------------------------------
uniform sampler2D Detail_D;



uniform sampler2D Main_D;



uniform sampler2D Main_N;



uniform sampler2D Detail_N;



uniform sampler2D Light0ShadowMap;

uniform sampler2D Light1ShadowMap;

uniform sampler2D Light2ShadowMap;








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

sampler2D GetLightShadowMap(int ActiveLightIndex) 
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
		return textureLod(Light0ShadowMap, UVs, 0); 
	else if (ActiveLightIndex == 1) 
		return textureLod(Light1ShadowMap, UVs, 0); 
	else 
		return textureLod(Light2ShadowMap, UVs, 0); 
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
#if defined(COMPILING_VS)
	in float3 IN_Position;
	in float2 IN_map2;
	in float2 IN_map1;
	in float3 IN_Tangent;
	in float3 IN_Normal;
	in float3 IN_BiNormal;
#endif 

	OUTIN float4 OUT_Position;
	OUTIN float4 OUT_map2;
	OUTIN float4 OUT_map1;
	OUTIN float4 OUT_Tangent;
	OUTIN float4 OUT_Normal;
	OUTIN float4 OUT_WorldPosition;

// -------------------------------------- CollapseRangeFunction --------------------------------------
struct CollapseRangeOutput
{
	float3 CollapsedVector;
};

CollapseRangeOutput CollapseRangeFunction(float3 Vector)
{
	CollapseRangeOutput OUT;

	float3 NormalMap = (0.5 * Vector);
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

	float3 MulOp = (Base * float3(2.0, 2.0, 2.0));
	float3 VarT = (MulOp + float3(-1.0, -1.0, 0.0));
	float3 MulOp1379 = (float3(-2.0, -2.0, 2.0) * Detail);
	float3 VarU = (MulOp1379 + float3(1.0, 1.0, -1.0));
	float3 MulOp1385 = (dot(VarT, VarU) * VarT);
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

	float3 NormalMap = (2.0 * Vector);
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

	float3 Bn = (TangentDirection * cross(Normal, Tangent));
	float3x3 toWorld = float3x3(Tangent, Bn, Normal);
	float3 TangentToWorld = (toWorld * Vector);
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

	float3 MulOp = ((LightColor * AlbedoColor) * LightIntensity);
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
	float3 LerpOp = mix((LightPosition - VertexWorldPosition), -(LightDirection), float(IsDirectionalLight));
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

	float SatOp = clamp(dot(Normal, LightVector), 0.0, 1.0);
	float3 Diffuse = (SatOp * AlbedoColor);
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
	float4 MulOp = (LightViewPrj * VectorConstruct);
	float3 DivOp = (MulOp.xyz / MulOp.w);
	if (DivOp.x > -1.0 && DivOp.x < 1.0 && DivOp.y > -1.0 && DivOp.y < 1.0 && DivOp.z > 0.0 && DivOp.z < 1.0)
	{
		float Val552 = 0.5;
		float2 AddOp = ((Val552 * DivOp.xy) + Val552);
		float SubOp = (DivOp.z - (ShadowMapBias / MulOp.w));
		float ShadowTotal = 0.0;
		for(int i=0; i<10; i+=1)
		{
			sampler2D _LightShadowMap = GetLightShadowMap(ActiveLightIndex);
			float2 MulOp604 = (0.00195313 * float2(1.0, 1.0));
			float4 Sampler = SampleFromShadowMap(ActiveLightIndex, (AddOp + MulOp604));
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
		float ShadowColorMix = mix(ShadowMap543.LightGain, 1.0, float(_LightShadowColor.x));
		ShadowMul530 = ShadowColorMix;
	}
	float DecayShadowConeMul = ((ShadowMul530 * ConeMul529) * DecayMul527);
	float3 LightColor = GetLightColor(ActiveLightIndex);
	float3 MulItensity = ((LightColor * DecayShadowConeMul) * _LightIntensity);
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
	float SatOp = clamp(dot(Normal, NormOp), 0.0, 1.0);
	float3 BlinnSpec = (SpecularColor * pow(SatOp, SpecularPower));
	float SatOp978 = clamp(dot(Normal, LightVector), 0.0, 1.0);
	float3 MulOp = (SatOp978 * BlinnSpec);
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
	float DotOp = dot(clamp(Color, 0.0, 1.0), Col.xyz);
	OUT.DesaturateColor = DotOp;

	return OUT;
}

// -------------------------------------- DesaturateColorFunction --------------------------------------
DesaturateColorOutput DesaturateColorFunction(float3 Color)
{
	DesaturateColorOutput OUT;

	float3 Col = float3(0.300008,0.6,0.100008);
	float DotOp = dot(clamp(Color, 0.0, 1.0), Col.xyz);
	OUT.DesaturateColor = DotOp;

	return OUT;
}

// -------------------------------------- ShaderVertex --------------------------------------
#if defined(COMPILING_VS)
	void main(void)
	{
		OUT_Position = float4(IN_Position, 1);
		float4 OutUVs = float4(IN_map2.x, IN_map2.y, 0.0, 0.0);
		OUT_map2 = OutUVs;
		float4 OutUVs1249 = float4(IN_map1.x, IN_map1.y, 0.0, 0.0);
		OUT_map1 = OutUVs1249;
		float3 MulOp = ((float3x3(world)) * IN_Tangent);
		float3 TangentNorm = normalize(MulOp);
		float4 WorldTangent = float4(TangentNorm.x, TangentNorm.y, TangentNorm.z, 1.0);
		OUT_Tangent = WorldTangent;
		float DotOp = dot(cross(IN_Normal, IN_Tangent), IN_BiNormal);
		float BiNormalDir1416 = (DotOp < 0.0) ? (-1.0) : (1.0);
		float4 VectorConstruct = float4(OUT_Tangent.xyz.x, OUT_Tangent.xyz.y, OUT_Tangent.xyz.z, BiNormalDir1416);
		OUT_Tangent = VectorConstruct;
		float3 MulOp1443 = ((float3x3(world)) * IN_Normal);
		float3 NormalN = normalize(MulOp1443);
		float4 WorldNormal = float4(NormalN.x, NormalN.y, NormalN.z, 1.0);
		OUT_Normal = WorldNormal;
		float4 WorldPos = (world * OUT_Position);
		OUT_WorldPosition = WorldPos;
		float4 WVSpace = (wvp * OUT_Position);
		OUT_Position = WVSpace;
	}
#endif 

// -------------------------------------- ShaderPixel --------------------------------------
#if defined(COMPILING_PS)
	out float4 OUT_Color;
#endif 

#if defined(COMPILING_PS)
	void main(void)
	{
		float InvertSatMask = (1.0 - clamp(0.0, 0.0, 1.0));
		float2 MulOp = (Val * OUT_map2.xy);
		float4 Sampler = texture(Detail_D, float2(MulOp.x, 1-MulOp.y));
		float4 Sampler1258 = texture(Main_D, float2(OUT_map1.xy.x, 1-OUT_map1.xy.y));
		float3 MulOp1304 = (Sampler1258.xyz * Sampler.xyz);
		float3 ReplaceDiffuseWithReflection = (MulOp1304 * InvertSatMask);
		float3 NormOp = normalize(OUT_Normal.xyz);
		float3 NormOp1461 = normalize(OUT_Tangent.xyz);
		float4 Sampler1607 = texture(Main_N, float2(OUT_map1.xy.x, 1-OUT_map1.xy.y));
		float4 Sampler1583 = texture(Detail_N, float2(MulOp.x, 1-MulOp.y));
		ReorientedNormalMappingOutput ReorientedNormalMapping1374 = ReorientedNormalMappingFunction(Sampler1607.xyz, Sampler1583.xyz);
		ExpandRangeOutput ExpandRange1475 = ExpandRangeFunction(ReorientedNormalMapping1374.Normal);
		float3 VectorConstruct = float3(1.0, 1.0, 1.0);
		float3 NormalMapH = (VectorConstruct.xyz * ExpandRange1475.ExpandedVector);
		TangentWorldConvertOutput TangentWorldConvert1462 = TangentWorldConvertFunction(OUT_Tangent.w, NormOp, NormOp1461, NormalMapH);
		float3 TangentSpace = normalize(TangentWorldConvert1462.Vector);
		float3 FlippedNormals = mix(-(TangentSpace), TangentSpace, float(gl_FrontFacing));
		float ClampOpacity = clamp(1.0, 0.0, 1.0);
		float3 CameraPosition = viewI[3].xyz;
		float3 CamVec = (CameraPosition - OUT_WorldPosition.xyz);
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
				float3 AmbientLightAndAO = (AmbientLight409.LightColor * 1.0);
				float4 VectorConstruct683 = float4(AmbientLightAndAO.x, AmbientLightAndAO.y, AmbientLightAndAO.z, 0.0);
				IfAmbientLight404 = VectorConstruct683;
			}
			else
			{
				float3 NoTranslucency = float3(0.0,0.0,0.0);
				float3 _LightPos = GetLightPos(ActiveLightIndex);
				float3 _LightDir = GetLightDir(ActiveLightIndex);
				GetLightVectorOutput GetLightVector851 = GetLightVectorFunction(ActiveLightIndex, _LightPos, OUT_WorldPosition.xyz, _LightType, _LightDir);
				float3 LightVecNorm = normalize(GetLightVector851.Result);
				LambertDiffuseOutput LambertDiffuse827 = LambertDiffuseFunction(ActiveLightIndex, ReplaceDiffuseWithReflection, FlippedNormals, LightVecNorm);
				LightContributionOutput LightContribution417 = LightContributionFunction(ActiveLightIndex, OUT_WorldPosition.xyz, GetLightVector851.Result);
				float3 AddTranslucency = (NoTranslucency.xyz + (LightContribution417.Light * LambertDiffuse827.Color));
				float3 Col = float3(1.0,1.0,1.0);
				BlinnSpecularOutput BlinnSpecular966 = BlinnSpecularFunction(ActiveLightIndex, LightVecNorm, FlippedNormals, CamVecNorm, 20.0, Col.xyz);
				float3 SpecLightIntensity = (BlinnSpecular966.SpecularColor * LightContribution417.Light);
				float3 Diffuse_Spec = ((ClampOpacity * AddTranslucency) + SpecLightIntensity);
				DesaturateColorOutput DesaturateColor675 = DesaturateColorFunction(ActiveLightIndex, SpecLightIntensity);
				float4 Color_Alpha = float4(Diffuse_Spec.x, Diffuse_Spec.y, Diffuse_Spec.z, DesaturateColor675.DesaturateColor);
				IfAmbientLight404 = Color_Alpha;
			}
			float4 ApplyWeight415 = IfAmbientLight404;
			LightLoopTotal11 += ApplyWeight415;
		}
		float3 NoReflection = float3(0.0,0.0,0.0);
		float3 ReflectXmask = (NoReflection.xyz * 0.0);
		float3 DefaultEmissiveColor = float3(0.0,0.0,0.0);
		float3 DefaultIBLColor = float3(0.0,0.0,0.0);
		float3 PreMultipliedAlpha = (ClampOpacity * (DefaultEmissiveColor.xyz + DefaultIBLColor.xyz));
		float3 AddReflection = (ReflectXmask + PreMultipliedAlpha);
		DesaturateColorOutput DesaturateColor384 = DesaturateColorFunction(ReflectXmask);
		float OpacityAndReflection = (ClampOpacity + DesaturateColor384.DesaturateColor);
		float4 TotalAmbientAndOpacity = float4(AddReflection.x, AddReflection.y, AddReflection.z, OpacityAndReflection);
		float4 LightLoopAndAfterLoop = (LightLoopTotal11 + TotalAmbientAndOpacity);
		float SatOp = clamp(LightLoopAndAfterLoop.w, 0.0, 1.0);
		float4 VectorConstruct31 = float4(LightLoopAndAfterLoop.xyz.x, LightLoopAndAfterLoop.xyz.y, LightLoopAndAfterLoop.xyz.z, SatOp);
		OUT_Color = VectorConstruct31;
	}
#endif 

