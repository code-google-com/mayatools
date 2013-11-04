


// This is the OLD Uber Shader left here for file backward compatibility
// The new shader is called: AutodeskUberShader.fx






// Maya 'Uber' Shader for DirectX 11, HLSL 5
//
// Copyright 2012 Autodesk, Inc.  All rights reserved.
// Use of this software is subject to the terms of the 
// Autodesk license agreement provided at the time of 
// installation or download, or which otherwise accompanies 
// this software in either electronic or hard copy form. 
//
// Thanks to:	Ben Cloward, Microsoft, AMD, NVidia (John McDonald & Bryan Dudash),
//				Vlachos et all, Colin Barre-Brisebois, John Hable. 


//------------------------------------
// Notes
// Maya uses 'pre-multiplied alpha' as its render state and this Uber Shader is build to work in unison with that.
// Alternatively, The dx11Shader node allows you to set your own render states by supplying the 'overridesDrawState' annotation in the technique
// You may find it harder to get proper transparency sorting if you choose to do so.
//
// The technique annotation 'isTransparent' is used to tell Maya how treat the technique with respect to transparency.
//	- If set to 0 the technique is always considered opaque
//	- If set to 1 the technique is always considered transparent
//	- If set to 2 the plugin will check if the parameter marked with the OPACITY semantic is less than 1.0
//	- If set to 3 the plugin will use the transparencyTest annotation to create a MEL procedure to perform the desired test.
// Maya will then render the object twice. Front faces follow by back faces.
//
// For some objects you may need to switch the Transparency Algorithm to 'Depth Peeling' to avoid transparency issues.
// Models that require this usually have internal faces.
//------------------------------------


//------------------------------------
// Defines
// how many mip map levels should Maya generate or load per texture. 
// 0 means all possible levels
// some textures may override this value, but most textures will follow whatever we have defined here
// If you wish to optimize performance (at the cost of reduced quality), you can set NumberOfMipMaps below to 1

#define NumberOfMipMaps 0

//------------------------------------




//------------------------------------
// State
//------------------------------------
RasterizerState WireframeCullFront
{
	CullMode = Front;
	FillMode = WIREFRAME;
};

BlendState PMAlphaBlending
{
    AlphaToCoverageEnable = FALSE;
	BlendEnable[0] = TRUE;
	SrcBlend = ONE;
	DestBlend = INV_SRC_ALPHA;
	BlendOp = ADD;
	SrcBlendAlpha = ONE;	// Required for hardware frame render alpha channel
	DestBlendAlpha = INV_SRC_ALPHA;
	BlendOpAlpha = ADD;
	RenderTargetWriteMask[0] = 0x0F;
};



//------------------------------------
// Samplers
//------------------------------------
SamplerState CubeMapSampler
{
	Filter = ANISOTROPIC;
	AddressU = Clamp;
	AddressV = Clamp;
	AddressW = Clamp;    
};

SamplerState SamplerAnisoWrap
{
	Filter = ANISOTROPIC;
	AddressU = Wrap;
	AddressV = Wrap;
};

SamplerState SamplerAnisoClamp
{
	Filter = ANISOTROPIC;
	AddressU = Clamp;
	AddressV = Clamp;
};

SamplerState SamplerShadowDepth
{
	Filter = MIN_MAG_MIP_POINT;
	AddressU = Border;
	AddressV = Border;
	BorderColor = float4(1.0f, 1.0f, 1.0f, 1.0f);
};


//------------------------------------
// Textures
//------------------------------------
Texture2D EmissiveTexture
<
	string UIGroup = "Ambient and Emissive";
	string ResourceName = "";
	string UIWidget = "FilePicker";
	string UIName = "Ambient Emissive Map";
	string ResourceType = "2D";
	int mipmaplevels = NumberOfMipMaps;
	int UIOrder = 101;
	int UVEditorOrder = 2;
>;

Texture2D DiffuseTexture
<
	string UIGroup = "Diffuse";
	string ResourceName = "";
	string UIWidget = "FilePicker";
	string UIName = "Diffuse Map";
	string ResourceType = "2D";	
	int mipmaplevels = NumberOfMipMaps;
	int UIOrder = 201;
	int UVEditorOrder = 1;
>;

Texture2D LightmapTexture
<
	string UIGroup = "Diffuse";
	string ResourceName = "";
	string UIWidget = "FilePicker";
	string UIName = "Lightmap Map";
	string ResourceType = "2D";	
	int mipmaplevels = NumberOfMipMaps;
	int UIOrder = 301;
	int UVEditorOrder = 3;
>;

Texture2D SpecularTexture
<
	string UIGroup = "Specular";
	string ResourceName = "";
	string UIWidget = "FilePicker";
	string UIName = "Specular Map";
	string ResourceType = "2D";
	int mipmaplevels = NumberOfMipMaps;
	int UIOrder = 401;
	int UVEditorOrder = 4;
>;

Texture2D NormalTexture
<
	string UIGroup = "Normal";
	string ResourceName = "";
	string UIWidget = "FilePicker";
	string UIName = "Normal Map";
	string ResourceType = "2D";
	int mipmaplevels = 0;	// If mip maps exist in texture, Maya will load them. So user can pre-calculate and re-normalize mip maps for normal maps in .dds
	int UIOrder = 501;
	int UVEditorOrder = 5;
>;

TextureCube CubeMapTexture : environment
<
	string UIGroup = "Reflection";
	string ResourceName = "";
	string UIWidget = "FilePicker";
	string UIName = "Reflection Cube Map";
	string ResourceType = "Cube";
	int mipmaplevels = 0; // Use (or load) max number of cubemaps so we can use blurring
	int UIOrder = 601;
	int UVEditorOrder = 6;
>;

Texture2D ReflectionMask
<
	string UIGroup = "Reflection";
	string ResourceName = "";
	string UIWidget = "FilePicker";
	string UIName = "Reflection Mask";
	string ResourceType = "2D";
	int mipmaplevels = NumberOfMipMaps;
	int UIOrder = 701;
	int UVEditorOrder = 7;
>;

Texture2D DisplacementTexture
<
	string UIGroup = "Tessellation and Displacement";
	string ResourceName = "";
	string UIWidget = "FilePicker";
	string UIName = "Displacement Map";
	string ResourceType = "2D";	
	int mipmaplevels = NumberOfMipMaps;
	int UIOrder = 801;
	int UVEditorOrder = 8;
>;

Texture2D TranslucencyThicknessMask
<
	string UIGroup = "Translucency";
	string ResourceName = "";
	string UIWidget = "FilePicker";
	string UIName = "Thickness Mask";
	string ResourceType = "2D";
	int mipmaplevels = NumberOfMipMaps;
	int UIOrder = 1001;
	int UVEditorOrder = 10;
>;

Texture2D SoftenDiffuseMask
<
	string UIGroup = "Diffuse";
	string ResourceName = "";
	string UIWidget = "FilePicker";
	string UIName = "Soften Diffuse Mask";
	string ResourceType = "2D";
	int mipmaplevels = NumberOfMipMaps;
	int UIOrder = 1101;
	int UVEditorOrder = 11;
>;

Texture2D OpacityMaskTexture
<
	string UIGroup = "Opacity";
	string ResourceName = "";
	string UIWidget = "FilePicker";
	string UIName = "Opacity Mask";
	string ResourceType = "2D";
	int mipmaplevels = NumberOfMipMaps;
	int UIOrder = 222;
	int UVEditorOrder = 12;
>;


//------------------------------------
// Shadow Maps
//------------------------------------
Texture2D light0ShadowMap : SHADOWMAP
<
	string Object = "Light 0";	// UI Group for lights, auto-closed
	string UIWidget = "None";
	int UIOrder = 5010;
>;

Texture2D light1ShadowMap : SHADOWMAP
<
	string Object = "Light 1";
	string UIWidget = "None";
	int UIOrder = 5020;
>;

Texture2D light2ShadowMap : SHADOWMAP
<
	string Object = "Light 2";
	string UIWidget = "None";
	int UIOrder = 5030;
>;



//------------------------------------
// Per Frame parameters
//------------------------------------
cbuffer UpdatePerFrame : register(b0)
{
	float4x4 viewInv 		: ViewInverse 			< string UIWidget = "None"; >;   
	float4x4 view			: View					< string UIWidget = "None"; >;
	float4x4 prj			: Projection			< string UIWidget = "None"; >;
	float4x4 viewPrj		: ViewProjection		< string UIWidget = "None"; >;

	// A shader may wish to do different actions when Maya is rendering the preview swatch (e.g. disable displacement)
	// This value will be true if Maya is rendering the swatch
	bool IsSwatchRender     : MayaSwatchRender      < string UIWidget = "None"; > = false;
}


//------------------------------------
// Per Object parameters
//------------------------------------
cbuffer UpdatePerObject : register(b1)
{
	float4x4 world 		: World 	< string UIWidget = "None"; >;


	// ---------------------------------------------
	// Lighting GROUP
	// ---------------------------------------------
	bool LinearSpaceLighting
	<
		string UIGroup = "Lighting";
		string UIName = "Linear Space Lighting";
		int UIOrder = 10;
	> = true;

	bool UseShadows
	<
		string UIGroup = "Lighting";
		string UIName = "Shadows";
		int UIOrder = 11;
	> = true;

	float shadowMultiplier
	<
		string UIGroup = "Lighting";
		string UIWidget = "Slider";
		float UIMin = 0.000;
		float UIMax = 1.000;
		float UIStep = 0.001;
		string UIName = "Shadow Strength";
		int UIOrder = 12;
	> = {1.0f};

	// This offset allows you to fix any in-correct self shadowing caused by limited precision.
	// This tends to get affected by scene scale and polygon count of the objects involved.
	float shadowDepthBias : ShadowMapBias
	<
		string UIGroup = "Lighting";
		string UIWidget = "Slider";
		float UIMin = 0.000;
		float UISoftMax = 10.000;
		float UIStep = 0.001;
		string UIName = "Shadow Bias";
		int UIOrder = 13;
	> = {0.01f};

	// flips back facing normals to improve lighting for things like sheets of hair or leaves
	bool flipBackfaceNormals
	<
		string UIGroup = "Lighting";
		string UIName = "Double Sided Lighting";
		int UIOrder = 14;
	> = true;


	// -- light props are inserted here via UIOrder 20 - 49


	float rimFresnelMin
	<
		string UIGroup = "Lighting";
		string UIWidget = "Slider";
		float UIMin = 0.0;
		float UIMax = 1.0;
		float UIStep = 0.001;
		string UIName = "Rim Light Min";
		int UIOrder = 60;
	> = 0.8;

	float rimFresnelMax
	<
		string UIGroup = "Lighting";
		string UIWidget = "Slider";
		float UIMin = 0.0;
		float UIMax = 1.0;
		float UIStep = 0.001;
		string UIName = "Rim Light Max";
		int UIOrder = 61;
	> = 1.0;

	float rimBrightness
	<
		string UIGroup = "Lighting";
		string UIWidget = "Slider";
		float UIMin = 0.0;
		float UISoftMax = 10.0;
		float UIStep = 0.001;
		string UIName = "Rim Light Brightness";
		int UIOrder = 62;
	> = 0.0;


	// ---------------------------------------------
	// Ambient and Emissive GROUP
	// ---------------------------------------------
	bool UseEmissiveTexture
	<
		string UIGroup = "Ambient and Emissive";
		string UIName = "Ambient Emissive Map";
		int UIOrder = 100;
	> = false;

	float3 AmbientSkyColor : Ambient
	<
		string UIGroup = "Ambient and Emissive";
		string UIName = "Ambient Sky Color";
		string UIWidget = "ColorPicker";
		int UIOrder = 103;
	> = {0.0f, 0.0f, 0.0f };

	float3 AmbientGroundColor : Ambient
	<
		string UIGroup = "Ambient and Emissive";
		string UIName = "Ambient Ground Color";
		string UIWidget = "ColorPicker";
		int UIOrder = 104;
	> = {0.0f, 0.0f, 0.0f };




	// ---------------------------------------------
	// Diffuse GROUP
	// ---------------------------------------------
	bool UseDiffuseTexture
	<
		string UIGroup = "Diffuse";
		string UIName = "Diffuse Map";
		int UIOrder = 199;
	> = false;

	bool UseDiffuseTextureAlpha
	<
		string UIGroup = "Diffuse";
		string UIName = "Diffuse Map Alpha";
		int UIOrder = 200;
	> = false;

	float3 DiffuseColor : Diffuse
	<
		string UIGroup = "Diffuse";
		string UIName = "Diffuse Color";
		string UIWidget = "ColorPicker";
		int UIOrder = 203;
	> = {1.0f, 1.0f, 1.0f };



	bool UseLightmapTexture
	<
		string UIGroup = "Diffuse";
		string UIName = "Lightmap Map";
		int UIOrder = 300;
	> = false;



	// blended normal
	bool UseBlendedNormalDiffuse
	<
		string UIGroup = "Diffuse";
		string UIName = "Soften Diffuse For Skin";
		int UIOrder = 1099;
	> = false;

	// This mask map allows you to control the amount of 'softening' that happens on different areas of the object
	bool UseSoftenDiffuseTexture
	<
		string UIGroup = "Diffuse";
		string UIName = "Soften Diffuse Mask";
		int UIOrder = 1100;
	> = false;

	float softenDiff
	<
		string UIGroup = "Diffuse";
		float UIMin = 0.0;
		float UISoftMax = 1.0;
		float UIStep = 0.1;
		string UIName   = "Soften Diffuse";
		int UIOrder = 1103;
	> = 0.15;



	// ---------------------------------------------
	// Opacity GROUP
	// ---------------------------------------------
	float Opacity : OPACITY
	<
		string UIGroup = "Opacity";
		string UIWidget = "Slider";
		float UIMin = 0.0;
		float UIMax = 1.0;
		float UIStep = 0.001;
		string UIName = "Opacity";
		int UIOrder = 220;
	> = 1.0;

	bool UseOpacityMaskTexture
	<
		string UIGroup = "Opacity";
		string UIName = "Opacity Mask";
		int UIOrder = 221;
	> = false;

	// at what value do we clip away pixels
	float OpacityMaskBias
	<
		string UIGroup = "Opacity";
		string UIWidget = "Slider";
		float UIMin = 0.0;
		float UIMax = 1.0;
		float UIStep = 0.001;
		string UIName = "Opacity Mask Bias";
		int UIOrder = 224;
	> = 0.1;



	// ---------------------------------------------
	// Specular GROUP
	// ---------------------------------------------
	bool UseSpecularTexture
	<
		string UIGroup = "Specular";
		string UIName = "Specular Map";
		int UIOrder = 400;
	> = false;

	float3 SpecularColor : Specular
	<
		string UIGroup = "Specular";
		string UIName = "Specular Color";
		string UIWidget = "ColorPicker";
		int UIOrder = 403;
	> = {1.0f, 1.0f, 1.0f };

	float SpecPower
	<
		string UIGroup = "Specular";
		string UIWidget = "Slider";
		float UIMin = 1.0;
		float UISoftMax = 100.0;
		float UIStep = 0.01;
		string UIName = "Specular Power";
		int UIOrder = 404;
	> = 20.0;

	bool UseKSSpecular
	<
		string UIGroup = "Specular";
		string UIName = "Kelemen-Szirmaykalos For Skin";
		int UIOrder = 405;
	> = false;



	// ---------------------------------------------
	// Normal GROUP
	// ---------------------------------------------
	bool UseNormalTexture
	<
		string UIGroup = "Normal";
		string UIName = "Normal Map";
		int UIOrder = 500;
	> = false;

	float NormalHeight
	<
		string UIGroup = "Normal";
		string UIWidget = "Slider";
		float UIMin = 0.0;
		float UISoftMax = 5.0;
		float UIStep = 0.01;
		string UIName = "Normal Height";
		int UIOrder = 503;
	> = 1.0;



	// ---------------------------------------------
	// Reflection GROUP
	// ---------------------------------------------
	bool UseCubeMap
	<
		string UIGroup = "Reflection";
		string UIName = "Reflection Cube Map";
		int UIOrder = 600;
	> = false;

	float ReflectionIntensity
	<
		string UIGroup = "Reflection";
		string UIWidget = "Slider";
		float UIMin = 0.0;
		float UISoftMax = 5.0;
		float UIStep = 0.001;
		string UIName = "Reflection Intensity";
		int UIOrder = 602;
	> = 0.2;

	float ReflectionBlur
	<
		string UIGroup = "Reflection";
		string UIWidget = "Slider";
		float UIMin = 0.0;
		float UISoftMax = 10.0;
		float UIStep = 0.001;
		string UIName = "Reflection Blur";
		int UIOrder = 603;
	> = 0.0;

	float ReflectionFresnelMin
	<
		string UIGroup = "Reflection";
		string UIWidget = "Slider";
		float UIMin = 0.0;
		float UIMax = 1.0;
		float UIStep = 0.001;
		string UIName = "Reflection Fresnel Min";
		int UIOrder = 604;
	> = 0.0;

	float ReflectionFresnelMax
	<
		string UIGroup = "Reflection";
		string UIWidget = "Slider";
		float UIMin = 0.0;
		float UIMax = 1.0;
		float UIStep = 0.001;
		string UIName = "Reflection Fresnel Max";
		int UIOrder = 605;
	> = 0.0;

	bool UseReflectionMask
	<
		string UIGroup = "Reflection";
		string UIName = "Reflection Mask";
		int UIOrder = 700;
	> = false;

	// When enabled uses the alpha channel of the specular texture to determine how much reflection needs to blur on parts of the object.
	// If this is disabled, the object's reflection is blurred equal amounts everywhere.
	bool UseSpecAlphaForReflectionBlur
	<
		string UIGroup = "Reflection";
		string UIName = "Spec Alpha For Reflection Blur";
		int UIOrder = 703;
	> = false;

	// When enabled, uses the specular color to tint the color of the cube map reflection.
	// When disabled, the cube map is not tinted and colors are used as found in the cube map.
	bool UseSpecColorToTintReflection
	<
		string UIGroup = "Reflection";
		string UIName = "Spec Color to Tint Reflection";
		int UIOrder = 704;
	> = false;



	// ---------------------------------------------
	// Tessellation and Displacement GROUP
	// ---------------------------------------------
	bool UseDisplacementMap
	<
		string UIGroup = "Tessellation and Displacement";
		string UIName = "Displacement Map";
		int UIOrder = 800;
	> = false;

	bool UseVectorDisplacement
	<
		string UIGroup = "Tessellation and Displacement";
		string UIName = "Tangent Vector Displacement";
		int UIOrder = 803;
	> = false;

	int VectorDisplacementCoordSys
	<		
		string UIGroup = "Tessellation and Displacement";
		string UIWidget = "Slider";
		int UIMin = 0;
		int UIMax = 1;
		int UIStep = 1;
		string UIFieldNames ="Mudbox (XZY):Maya (XYZ)";
		string UIName = "Displacement Coordsys";
		int UIOrder = 804;
	> = 0;

	float DisplacementHeight
	<
		string UIGroup = "Tessellation and Displacement";
		float UISoftMin = 0.0;
		float UISoftMax = 10.0;
		string UIName = "Displacement Height";
		int UIOrder = 805;
	> = 0.5;

	// This allows you to control what the 'base' value for displacement is.
	// When the offset value is 0.5, that means that a gray value (color: 128,128,128) will get 0 displacement.
	// A value of 0 would then dent in.
	// A value of 1 would then extrude.
	float DisplacementOffset
	<
		string UIGroup = "Tessellation and Displacement";
		float UISoftMin = -1.0;
		float UISoftMax = 1.0;
		string UIName = "Displacement Offset";
		int UIOrder = 806;
	> = 0.5;

	// This gives the artist control to prevent this shader from clipping away faces to quickly when displacement is actually keeping the faces on screen.
	// This is also important for e.g. shadow map generation to make sure displaced vertices are not clipped out of the light's view
	// See BBoxExtraScale for artist control over Maya clipping the entire object away when it thinks it leaves the view.
	float DisplacementClippingBias
	<
		string UIGroup = "Tessellation and Displacement";
		float UISoftMin = 0.0;
		float UISoftMax = 99.0;
		string UIName = "Displacement Clipping Bias";
		int UIOrder = 807;
	> = 5.0;

	// This gives the artist control to prevent maya from clipping away the entire object to fast in case displacement is used.
	// Its semantic has to be BoundingBoxExtraScale
	float BBoxExtraScale : BoundingBoxExtraScale
	<
		string UIGroup = "Tessellation and Displacement";
		float UIMin = 1.0;
		float UISoftMax = 10.0;
		string UIName = "Bounding Box Extra Scale";
		int UIOrder = 808;
	> = 1.0;

	float TessellationRange
	<
		string UIGroup = "Tessellation and Displacement";
		string UIWidget = "Slider";
		float UIMin = 0.0;
		float UISoftMax = 999.0;
		float UIStep = 0.01;
		string UIName = "Tessellation Range";
		int UIOrder = 809;
	> = {0};

	float TessellationMin
	<
		string UIGroup = "Tessellation and Displacement";
		float UIMin = 1.0;
		float UISoftMax = 10.0;
		string UIName = "Tessellation Minimum";
		int UIOrder = 810;
	> = 3.0;

	float FlatTessellation
	<
		string UIGroup = "Tessellation and Displacement";
		float UIMin = 0.0;
		float UIMax = 1.0;
		string UIName = "Flat Tessellation";
		int UIOrder = 811;
	> = 0.0;



	// ---------------------------------------------
	// Translucency GROUP
	// ---------------------------------------------
	bool UseTranslucency
	<
		string UIGroup = "Translucency";
		string UIName = "Translucency";
		int UIOrder = 999;
	> = false;

	bool UseThicknessTexture
	<
		string UIGroup = "Translucency";
		string UIName = "Thickness Mask";
		int UIOrder = 1000;
	> = false;

	// This determines how much the normal (per pixel) influences the translucency.
	// If this value is 0, then the translucency is very uniform over the entire object.
	// Meaning: the object is translucent the same amount everywhere (although the thickness map will still be in affect, if you use one)
	// If the value is higher, for example 0.5. This means the translucent effect is broken up (distorted) based on the normal. 
	// The result will feel more organic.
	float translucentDistortion
	<
		string UIGroup = "Translucency";
		string UIWidget = "Spinner";
		float UIMin = 0.0;
		float UISoftMax = 10.0;
		float UIStep = 0.05;
		string UIName = "Light Translucent Distortion";
		int UIOrder = 1003;
	> = 0.2;

	// This changes the focus or size of the translucent areas. 
	// Similar to how you can change the size of specular reflection by changing the specular power (aka Specular Glossiness).
	float translucentPower
	<
		string UIGroup = "Translucency";
		string UIWidget = "Spinner";
		float UIMin = 0.0;
		float UISoftMax = 20.0;
		float UIStep = 0.01;
		string UIName = "Light Translucent Power";
		int UIOrder = 1004;
	> = 3.0;

	// This is to adjust the amount of translucency caused by the light(s) behind the object.
	float translucentScale
	<
		string UIGroup = "Translucency";
		string UIWidget = "Spinner";
		float UIMin = 0.0;
		float UISoftMax = 1.0;
		float UIStep = 0.01;
		string UIName = "Light Translucent Scale";
		int UIOrder = 1005;
	> = 1.0;

	// This is the translucency the object always has, even if no light is directly behind it.
	float translucentMin
	<
		string UIGroup = "Translucency";
		string UIWidget = "Spinner";
		float UIMin = 0.0;
		float UISoftMax = 1.0;
		float UIStep = 0.01;
		string UIName = "Translucent Minimum";
		int UIOrder = 1006;
	> = 0.0;

	float3 SkinRampOuterColor
	<
		string UIGroup = "Translucency";
		string UIName = "Outer Translucent Color";
		string UIWidget = "ColorPicker";
		int UIOrder = 1007;
	> = {1.0f, 0.64f, 0.25f };

	float3 SkinRampMediumColor
	<
		string UIGroup = "Translucency";
		string UIName = "Medium Translucent Color";
		string UIWidget = "ColorPicker";
		int UIOrder = 1008;
	> = {1.0f, 0.21f, 0.14f };

	float3 SkinRampInnerColor
	<
		string UIGroup = "Translucency";
		string UIName = "Inner Translucent Color";
		string UIWidget = "ColorPicker";
		int UIOrder = 1009;
	> = {0.25f, 0.05f, 0.02f };


	// ---------------------------------------------
	// UV assignment GROUP
	// ---------------------------------------------
	// Use the Surface Data Section to set your UVset names for each Texcoord.
	// E.g. TexCoord1 = uv:UVset
	// Then pick a Texcoord in the UV Section to use that UVset for a texture.

	int EmissiveTexcoord
	<		
		string UIGroup = "UV";
		string UIWidget = "Slider";
		int UIMin = 0;
		int UIMax = 2;
		int UIStep = 1;
		string UIFieldNames ="TexCoord0:TexCoord1:TexCoord2";
		string UIName = "Ambient Emissive Map";
		int UIOrder = 2001;
	> = 0;

	int DiffuseTexcoord
	<		
		string UIGroup = "UV";
		string UIWidget = "Slider";
		int UIMin = 0;
		int UIMax = 2;
		int UIStep = 1;
		string UIFieldNames ="TexCoord0:TexCoord1:TexCoord2";
		string UIName = "Diffuse Map";
		int UIOrder = 2002;
	> = 0;

	int LightmapTexcoord
	<		
		string UIGroup = "UV";
		string UIWidget = "Slider";
		int UIMin = 0;
		int UIMax = 2;
		int UIStep = 1;
		string UIFieldNames ="TexCoord0:TexCoord1:TexCoord2";
		string UIName = "Light Map";
		int UIOrder = 2003;
	> = 1;

	int SoftenDiffuseMaskTexcoord
	<		
		string UIGroup = "UV";
		string UIWidget = "Slider";
		int UIMin = 0;
		int UIMax = 2;
		int UIStep = 1;
		string UIFieldNames ="TexCoord0:TexCoord1:TexCoord2";
		string UIName = "Soften Mask";
		int UIOrder = 2004;
	> = 0;

	int OpacityMaskTexcoord
	<		
		string UIGroup = "UV";
		string UIWidget = "Slider";
		int UIMin = 0;
		int UIMax = 2;
		int UIStep = 1;
		string UIFieldNames ="TexCoord0:TexCoord1:TexCoord2";
		string UIName = "Opacity Mask";
		int UIOrder = 2005;
	> = 0;

	int SpecularTexcoord
	<		
		string UIGroup = "UV";
		string UIWidget = "Slider";
		int UIMin = 0;
		int UIMax = 2;
		int UIStep = 1;
		string UIFieldNames ="TexCoord0:TexCoord1:TexCoord2";
		string UIName = "Specular Map";
		int UIOrder = 2006;
	> = 0;

	int NormalTexcoord
	<		
		string UIGroup = "UV";
		string UIWidget = "Slider";
		int UIMin = 0;
		int UIMax = 2;
		int UIStep = 1;
		string UIFieldNames ="TexCoord0:TexCoord1:TexCoord2";
		string UIName = "Normal Map";
		int UIOrder = 2007;
	> = 0;

	int ReflectionMaskTexcoord
	<		
		string UIGroup = "UV";
		string UIWidget = "Slider";
		int UIMin = 0;
		int UIMax = 2;
		int UIStep = 1;
		string UIFieldNames ="TexCoord0:TexCoord1:TexCoord2";
		string UIName = "Reflection Mask";
		int UIOrder = 2008;
	> = 0;

	int DisplacementTexcoord
	<		
		string UIGroup = "UV";
		string UIWidget = "Slider";
		int UIMin = 0;
		int UIMax = 2;
		int UIStep = 1;
		string UIFieldNames ="TexCoord0:TexCoord1:TexCoord2";
		string UIName = "Displacement Map";
		int UIOrder = 2009;
	> = 0;

	int ThicknessTexcoord
	<		
		string UIGroup = "UV";
		string UIWidget = "Slider";
		int UIMin = 0;
		int UIMax = 2;
		int UIStep = 1;
		string UIFieldNames ="TexCoord0:TexCoord1:TexCoord2";
		string UIName = "Translucency Mask";
		int UIOrder = 2010;
	> = 0;


} //end UpdatePerObject cbuffer



//------------------------------------
// Light parameters
//------------------------------------
cbuffer UpdateLights : register(b2)
{
	// ---------------------------------------------
	// Light 0 GROUP
	// ---------------------------------------------
	// This value is controlled by Maya to tell us if a light should be calculated
	// For example the artist may disable a light in the scene, or choose to see only the selected light
	// This flag allows Maya to tell our shader not to contribute this light into the lighting
	bool light0Enable : LIGHTENABLE
	<
		string Object = "Light 0";	// UI Group for lights, auto-closed
		string UIName = "Enable Light 0";
		int UIOrder = 20;
	> = false;

	// follows LightParameterInfo::ELightType
	// spot = 2, point = 3, directional = 4, ambient = 5,
	int light0Type : LIGHTTYPE
	<
		string Object = "Light 0";
		string UIName = "Light 0 Type";
		string UIWidget = "None";
		int UIOrder = 21;
	> = 2;	// default to spot so the cone angle etc work when "Use Shader Settings" option is used

	float3 light0Pos : POSITION 
	< 
		string Object = "Light 0";
		string UIName = "Light 0 Position"; 
		string Space = "World"; 
		int UIOrder = 22;
	> = {100.0f, 100.0f, 100.0f}; 

	float3 light0Color : LIGHTCOLOR 
	<
		string Object = "Light 0";
		string UIName = "Light 0 Color"; 
		string UIWidget = "Color"; 
		int UIOrder = 23;
	> = { 1.0f, 1.0f, 1.0f};

	float light0Intensity : LIGHTINTENSITY 
	<
		string Object = "Light 0";
		string UIName = "Light 0 Intensity"; 
		int UIOrder = 24;
	> = { 1.0f };

	float3 light0Dir : DIRECTION 
	< 
		string Object = "Light 0";
		string UIName = "Light 0 Direction"; 
		string Space = "World"; 
		int UIOrder = 25;
	> = {100.0f, 100.0f, 100.0f}; 

	float light0ConeAngle : HOTSPOT 
	<
		string Object = "Light 0";
		string UIName = "Light 0 Cone Angle"; 
		int UIOrder = 26;
	> = { 45.0f };

	float light0FallOff : FALLOFF 
	<
		string Object = "Light 0";
		string UIName = "Light 0 Penumbra Angle"; 
		int UIOrder = 27;
	> = { 0.0f };

	float light0AttenScale : DECAYRATE
	<
		string Object = "Light 0";
		string UIName = "Light 0 Decay";
		int UIOrder = 28;
	> = {0.0};

	bool light0ShadowOn : SHADOWFLAG
	<
		string Object = "Light 0";
		string UIName = "Light 0 Casts Shadow";
		string UIWidget = "None";
		int UIOrder = 29;
	> = true;

	float4x4 light0Matrix : SHADOWMAPMATRIX		
	< 
		string Object = "Light 0";
		string UIWidget = "None"; 
	>;



	// ---------------------------------------------
	// Light 1 GROUP
	// ---------------------------------------------
	bool light1Enable : LIGHTENABLE
	<
		string Object = "Light 1";
		string UIName = "Enable Light 1";
		int UIOrder = 30;
	> = false;

	int light1Type : LIGHTTYPE
	<
		string Object = "Light 1";
		string UIName = "Light 1 Type";
		string UIWidget = "None";
		int UIOrder = 31;
	> = 2;

	float3 light1Pos : POSITION 
	< 
		string Object = "Light 1";
		string UIName = "Light 1 Position"; 
		string Space = "World"; 
		int UIOrder = 32;
	> = {-100.0f, 100.0f, 100.0f}; 

	float3 light1Color : LIGHTCOLOR 
	<
		string Object = "Light 1";
		string UIName = "Light 1 Color"; 
		string UIWidget = "Color"; 
		int UIOrder = 33;
	> = { 1.0f, 1.0f, 1.0f};

	float light1Intensity : LIGHTINTENSITY 
	<
		string Object = "Light 1";
		string UIName = "Light 1 Intensity"; 
		int UIOrder = 34;
	> = { 1.0f };

	float3 light1Dir : DIRECTION 
	< 
		string Object = "Light 1";
		string UIName = "Light 1 Direction"; 
		string Space = "World"; 
		int UIOrder = 35;
	> = {100.0f, 100.0f, 100.0f}; 

	float light1ConeAngle : HOTSPOT 
	<
		string Object = "Light 1";
		string UIName = "Light 1 Cone Angle"; 
		int UIOrder = 36;
	> = { 45.0f };

	float light1FallOff : FALLOFF 
	<
		string Object = "Light 1";
		string UIName = "Light 1 Penumbra Angle"; 
		int UIOrder = 37;
	> = { 0.0f };

	float light1AttenScale : DECAYRATE
	<
		string Object = "Light 1";
		string UIName = "Light 1 Decay";
		int UIOrder = 38;
	> = {0.0};

	bool light1ShadowOn : SHADOWFLAG
	<
		string Object = "Light 1";
		string UIName = "Light 1 Casts Shadow";
		string UIWidget = "None";
		int UIOrder = 39;
	> = true;

	float4x4 light1Matrix : SHADOWMAPMATRIX		
	< 
		string Object = "Light 1";
		string UIWidget = "None"; 
	>;



	// ---------------------------------------------
	// Light 2 GROUP
	// ---------------------------------------------
	bool light2Enable : LIGHTENABLE
	<
		string Object = "Light 2";
		string UIName = "Enable Light 2";
		int UIOrder = 40;
	> = false;

	int light2Type : LIGHTTYPE
	<
		string Object = "Light 2";
		string UIName = "Light 2 Type";
		string UIWidget = "None";
		int UIOrder = 41;
	> = 2;

	float3 light2Pos : POSITION 
	< 
		string Object = "Light 2";
		string UIName = "Light 2 Position"; 
		string Space = "World"; 
		int UIOrder = 42;
	> = {100.0f, 100.0f, -100.0f}; 

	float3 light2Color : LIGHTCOLOR 
	<
		string Object = "Light 2";
		string UIName = "Light 2 Color"; 
		string UIWidget = "Color"; 
		int UIOrder = 43;
	> = { 1.0f, 1.0f, 1.0f};

	float light2Intensity : LIGHTINTENSITY 
	<
		string Object = "Light 2";
		string UIName = "Light 2 Intensity"; 
		int UIOrder = 44;
	> = { 1.0f };

	float3 light2Dir : DIRECTION 
	< 
		string Object = "Light 2";
		string UIName = "Light 2 Direction"; 
		string Space = "World"; 
		int UIOrder = 45;
	> = {100.0f, 100.0f, 100.0f}; 

	float light2ConeAngle : HOTSPOT 
	<
		string Object = "Light 2";
		string UIName = "Light 2 Cone Angle"; 
		int UIOrder = 46;
	> = { 45.0f };

	float light2FallOff : FALLOFF 
	<
		string Object = "Light 2";
		string UIName = "Light 2 Penumbra Angle"; 
		int UIOrder = 47;
	> = { 0.0f };

	float light2AttenScale : DECAYRATE
	<
		string Object = "Light 2";
		string UIName = "Light 2 Decay";
		int UIOrder = 48;
	> = {0.0};

	bool light2ShadowOn : SHADOWFLAG
	<
		string Object = "Light 2";
		string UIName = "Light 2 Casts Shadow";
		string UIWidget = "None";
		int UIOrder = 49;
	> = true;

	float4x4 light2Matrix : SHADOWMAPMATRIX		
	< 
		string Object = "Light 2";
		string UIWidget = "None"; 
	>;

} //end lights cbuffer



//------------------------------------
// Structs
//------------------------------------
struct APPDATA
{ 
	float3 position		: POSITION;
	float2 texCoord0	: TEXCOORD0; 
	float2 texCoord1	: TEXCOORD1; 
	float2 texCoord2	: TEXCOORD2;
	float3 normal		: NORMAL;
	float3 binormal		: BINORMAL;
	float3 tangent		: TANGENT; 
};

struct SHADERDATA
{
	float4 position			: SV_Position;
	float2 texCoord0		: TEXCOORD0; 
	float2 texCoord1		: TEXCOORD1;
	float2 texCoord2		: TEXCOORD2;
	float3 worldNormal   	: NORMAL;
	float4 worldTangent 	: TANGENT; 
	float3 worldPosition	: TEXCOORD3;

	// Geometry generated control points:
	// .worldPosition is CP0, so we don't need to store it again
	float3 CP1    : TEXCOORD4;
	float3 CP2    : TEXCOORD5;

	// PN-AEN with displacement fix:
	float4 dominantEdge    : TEXCOORD6;	// both vertices of an edge
	float2 dominantVertex  : TEXCOORD7;	// corner

	// Dominant normal and tangent for VDM crack fix:
	// this could be compacted into less texcoords, but left as-is for readability
	float3 dominantNormalE0 : TEXCOORD8;
	float3 dominantNormalE1 : TEXCOORD9;
	float3 dominantNormalCorner : TEXCOORD10;

	float3 dominantTangentE0 : TEXCOORD11;
	float3 dominantTangentE1 : TEXCOORD12;
	float3 dominantTangentCorner : TEXCOORD13;

	float clipped : CLIPPED;
};


struct HSCONSTANTDATA
{
	float TessFactor[3]		: SV_TessFactor;		// tessellation amount for each edge of patch
	float InsideTessFactor	: SV_InsideTessFactor;	// tessellation amount within a patch surface (would be float2 for quads)
	float3 CPCenter			: CENTER;				// Geometry generated center control point
};



//------------------------------------
// Functions
//------------------------------------

float2 pickTexcoord(int index, float2 t0, float2 t1, float2 t2)
{
	float2 tcoord = t0;

	if (index == 1)
		tcoord = t1;
	else if (index == 2)
		tcoord = t2;

	return tcoord;
}


// Spot light cone
float lightConeangle(float coneAngle, float coneFalloff, float3 lightVec, float3 lightDir) 
{ 
	float LdotDir = dot(normalize(lightVec), -lightDir); 

	// cheaper cone, no fall-off control would be:
	// float cone = pow(saturate(LdotDir), 1 / coneAngle); 

	// higher quality cone (more expensive):
	float cone = smoothstep( cos(coneFalloff), cos(coneAngle), LdotDir);

	return cone; 
} 


#define SHADOW_FILTER_TAPS_CNT 10
float2 SuperFilterTaps[SHADOW_FILTER_TAPS_CNT] 
< 
	string UIWidget = "None"; 
> = 
{ 
    {-0.84052f, -0.073954f}, 
    {-0.326235f, -0.40583f}, 
    {-0.698464f, 0.457259f}, 
    {-0.203356f, 0.6205847f}, 
    {0.96345f, -0.194353f}, 
    {0.473434f, -0.480026f}, 
    {0.519454f, 0.767034f}, 
    {0.185461f, -0.8945231f}, 
    {0.507351f, 0.064963f}, 
    {-0.321932f, 0.5954349f} 
};

float shadowMapTexelSize 
< 
	string UIWidget = "None"; 
> = {0.00195313}; // (1.0f / 512)

// Shadows:
// Percentage-Closer Filtering
float lightShadow(float4x4 LightViewPrj, uniform Texture2D ShadowMapTexture, float3 VertexWorldPosition)
{	
	float shadow = 1.0f;

	float4 Pndc = mul( float4(VertexWorldPosition.xyz,1.0) ,  LightViewPrj); 
	Pndc.xyz /= Pndc.w; 
	if ( Pndc.x > -1.0f && Pndc.x < 1.0f && Pndc.y  > -1.0f   
		&& Pndc.y <  1.0f && Pndc.z >  0.0f && Pndc.z <  1.0f ) 
	{ 
		float2 uv = 0.5f * Pndc.xy + 0.5f; 
		uv = float2(uv.x,(1.0-uv.y));	// maya flip Y
		float z = Pndc.z - shadowDepthBias / Pndc.w; 

		// we'll sample a bunch of times to smooth our shadow a little bit around the edges:
		shadow = 0.0f;
		for(int i=0; i<SHADOW_FILTER_TAPS_CNT; ++i) 
		{ 
			float2 suv = uv + (SuperFilterTaps[i] * shadowMapTexelSize);
			float val = z - ShadowMapTexture.SampleLevel(SamplerShadowDepth, suv, 0 ).x;
			shadow += (val >= 0.0f) ? 0.0f : (1.0f / SHADOW_FILTER_TAPS_CNT);
		}

		// a single sample would be:
		// shadow = 1.0f;
		// float val = z - ShadowMapTexture.SampleLevel(SamplerShadowDepth, uv, 0 ).x;
		// shadow = (val >= 0.0f)? 0.0f : 1.0f;
		
		shadow = lerp(1.0f, shadow, shadowMultiplier);  
	} 

	return shadow;
}


// This function is a modified version of Colin Barre-Brisebois GDC talk
float3 translucency(float3 thickness, float3 V, float3 L, float3 N, float lightAttenuation, 
					float gammaCorrection, float3 albedoColor)
{
	float3 LightVec = L + (N * translucentDistortion);
	float fLTDot = pow(saturate(dot(V,-LightVec)), translucentPower) * translucentScale;
	float3 translucence = lightAttenuation * (fLTDot + translucentMin) * thickness;

	float3 skinDepthColor = albedoColor * translucence;

	// if the outcolor is set to complete black, we assume user does not want to use ramp
	// We'll then use the above: albedo * translucence
	if (SkinRampOuterColor.r > 0 && SkinRampOuterColor.g > 0 && SkinRampOuterColor.b > 0)
	{
		if (translucence.r > 0.9)
		{
			skinDepthColor = lerp( SkinRampOuterColor, float3(1,1,1), (translucence.r-0.9)/0.1);
		}
		else if (translucence.r > 0.7)
		{
			skinDepthColor = lerp( SkinRampMediumColor, SkinRampOuterColor, (translucence.r-0.7)/0.2);
		}
		else if (translucence.r > 0.4)
		{
			skinDepthColor = lerp( SkinRampInnerColor, SkinRampMediumColor, (translucence.r-0.4)/0.3);
		}
		else
		{
			skinDepthColor = lerp( float3(0,0,0), SkinRampInnerColor, translucence.r/0.4);
		}

		skinDepthColor = pow( skinDepthColor, gammaCorrection);
	}

	return skinDepthColor;
}

// This function is from Nvidia's Human Head demo
float fresnelReflectance( float3 H, float3 V, float F0 )  
{
	float base = 1.0 - dot( V, H );
	float exponential = pow( base, 5.0 );  
	return exponential + F0 * ( 1.0 - exponential );
}

// This function is from Nvidia's Human Head demo
float beckmannBRDF(float ndoth, float m)
{
  float alpha = acos( ndoth );  
  float ta = tan( alpha );  
  float val = 1.0/(m*m*pow(ndoth,4.0)) * exp(-(ta*ta)/(m*m));
  return val;  
}

// This function is from Nvidia's Human Head demo
float3 KelemenSzirmaykalosSpecular(float3 N, float3 L, float3 V, float roughness, float3 specularColorIn)
{
	float3 result = float3(0.0, 0.0, 0.0);
	float ndotl = dot(N, L);
	if (ndotl > 0.0)
	{
		float3 h = L + V;
		float3 H = normalize( h );
		float ndoth = dot(N, H);
		float PH = beckmannBRDF(ndoth, roughness);
		float F = fresnelReflectance( H, V, 0.028 );
		float frSpec = max( PH * F / dot( h, h ), 0 ); 
		result = ndotl * specularColorIn * frSpec;
	}
	return result;
}

// This function is from John Hable's Siggraph talk
float3 blendedNormalDiffuse(float3 L, float3 Ng, float3 Nm, float softenMask, float shadow)
{
	float redBlend = lerp(0, 0.9, softenMask);
	float redSoften = redBlend * softenDiff;
	float blueBlend = lerp(0, 0.35, softenMask);
	float blueSoften = blueBlend * softenDiff;
	
	float DNr = (saturate(dot(Ng, L) * (1 - redSoften) + redSoften) * shadow);//diffuse using geometry normal
	float DNb = (saturate(dot(Nm, L) * (1 - blueSoften) + blueSoften) * shadow);//diffuse using normal map
	float R = lerp(DNb, DNr, redBlend);//final diffuse for red channel using more geometry normal
	float B = lerp(DNb, DNr, blueBlend);//final diffuse for blue using more normal map
	float3 finalDiffuse = float3(R, B, B);
	float cyanReduction = 0.03 + R;
	finalDiffuse.gb = min(cyanReduction, finalDiffuse.gb);
	return finalDiffuse;
}

// Pick dominant for crack free displacement (original function by Bryan Dudash, modified to support any float3)
float3 PickDominant( float3 vec,			// vector to change
				float U, float V, float W,	// barycoords
				float3 DE0A, float3 DE0B,	// domimant edge 0 vertex A and B
				float3 DE1A, float3 DE1B,	// domimant edge 1 vertex A and B
				float3 DE2A, float3 DE2B,	// domimant edge 2 vertex A and B
				float3 DV0, float3 DV1, float3 DV2 )	// dominant corners
{
	// Override the texture coordinates along the primitive edges and at the corners.  
	// Keep the original interpolated coords for the inner area of the primitive.

	float3 dominantVector = vec;

	float edgeThreshold = 0.0001f;
	float edgeU = (U == 0) ? 1 : 0;
	float edgeV = (V == 0) ? 1 : 0;
	float edgeW = (W == 0) ? 1 : 0;

	float corner = ((edgeU + edgeV + edgeW) == 2) ? 1 : 0;		// two are 0, means we are a corner
	float edge   = ((edgeU + edgeV + edgeW) == 1) ? 1 : 0;		// one of them is 0, means we are an edge
	float innerarea = ((edgeU + edgeV + edgeW) == 0) ? 1 : 0;	// none are 0, means we are interior

	if (innerarea != 1)
	{
		// Note: the order of the vertices/edges we choose here can be different per application
		//		 and depend on how the index buffer was generated.
		//		 These work for Maya with its PN-AEN18 primitive generator
		if (corner)
		{
			if (U > 1.0 - edgeThreshold)
				dominantVector = DV1;
			else if (V > 1.0 - edgeThreshold)
				dominantVector = DV2;
			else if (W > 1.0 - edgeThreshold)
				dominantVector = DV0;	
		}
		else
		{
			if (edgeU)
				dominantVector = lerp(DE2A, DE2B, W);
			else if (edgeV)
				dominantVector = lerp(DE0A, DE0B, U);
			else 
				dominantVector = lerp(DE1A, DE1B, V);
		}
	}

	return dominantVector;
}

// outside of view?
float IsClipped(float4 clipPos)
{
	float W = clipPos.w + DisplacementClippingBias;	// bias allows artist to control to early clipping due to displacement
    // Test whether the position is entirely inside the view frustum.
    return (-W <= clipPos.x && clipPos.x <= W
         && -W <= clipPos.y && clipPos.y <= W
         && -W <= clipPos.z && clipPos.z <= W)
       ? 0.0f
       : 1.0f;
}

// Compute whether all three control points along the edge are outside of the view frustum.
// By doing this, we're ensuring that 
// 1.0 means clipped, 0.0 means unclipped.
float ComputeClipping(float3 cpA, float3 cpB, float3 cpC)
{
    // Compute the projected position for each position, then check to see whether they are clipped.
    float4 projPosA = mul( float4(cpA,1), viewPrj ),
           projPosB = mul( float4(cpB,1), viewPrj ),
           projPosC = mul( float4(cpC,1), viewPrj );
     
    return min(min(IsClipped(projPosA), IsClipped(projPosB)), IsClipped(projPosC));
}

// PN Triangles and PN-AEN control points:
float3 ComputeCP(float3 posA, float3 posB, float3 normA) 
{
    return (2.0f * posA + posB - (dot((posB - posA), normA) * normA)) / 3.0f;
}

// Clip pixel away when opacity mask is used
void OpacityMaskClip(float2 uv)
{
	if (UseOpacityMaskTexture)
	{
		float OpacityMaskMap = OpacityMaskTexture.Sample(SamplerAnisoWrap, uv).x;

		// clip value when less then 0 for punch-through alpha.
		clip( OpacityMaskMap < OpacityMaskBias ? -1:1 );
	}
}

// Calculate a light:
struct lightOut
{
	float Specular;
	float3 Color;
};

lightOut CalculateLight	(	bool lightEnable, int lightType, float lightAtten, float3 lightPos, float3 vertWorldPos, 
							float3 lightColor, float lightIntensity, float3 lightDir, float lightConeAngle, float lightFallOff, float4x4 lightViewPrjMatrix, 
							uniform Texture2D lightShadowMap, bool lightShadowOn, float3 vertexNormal, float3 normal, float3 diffuseColorIn, 
							float3 eyeVec, float roughness,	float3 specularColorIn, float3 thickness, float softenMask, 
							float gammaCorrection, float rim, float glossiness, float opacity )
{
	lightOut OUT = (lightOut)0;

	OUT.Specular = 0.0;
	OUT.Color = float3(0,0,0);

	if (lightEnable)
	{
		// Ambient light does no diffuse, specular shading or shadow casting.
		// Because it does equal shading from all directions to the object, we will also not have it do any translucency.
		bool isAmbientLight = (lightType == 5);
		if (isAmbientLight)
		{
			OUT.Color = diffuseColorIn * lightColor * lightIntensity;
			return OUT;
		}

		// directional light has no position, so we use lightDir instead
		bool isDirectionalLight = (lightType == 4);
		float3 lightVec = lerp(lightPos - vertWorldPos, -lightDir, isDirectionalLight);

		float3 L = normalize(lightVec);	

		// Diffuse:
		float3 diffuseColor = float3(0,0,0);
		if (!UseBlendedNormalDiffuse)
		{
			// Lambert:
			diffuseColor = saturate(dot(normal, L)) * diffuseColorIn;
		}
		else
		{
			// Blended Normal, softens diffuse for skin:
			diffuseColor = blendedNormalDiffuse(L, vertexNormal, normal, softenMask, 1.0) * diffuseColorIn;
		}

		// Rim Light:
		float3 rimColor = rim * saturate(dot(normal, -L));	 

		// Specular:
		float3 specularColor = float3(0,0,0);

		if (!UseKSSpecular)
		{
			// Phong:
			// float3 R = -reflect(L, normal); 
			// float RdotV = saturate(dot(R,eyeVec));
			// specularColor = (pow(RdotV, glossiness) * specularColorIn);

			// Blinn:
			float3 H = normalize(L + eyeVec); // half angle
			float NdotH = saturate( dot(normal, H) );
			specularColor = specularColorIn * pow(NdotH, glossiness);
			specularColor *= saturate( dot(normal, L) );	// prevent spec leak on back side of model
		}
		else
		{
			// Kelemen/Szirmay-Kalos:
			specularColor = KelemenSzirmaykalosSpecular(normal, L, eyeVec, roughness, specularColorIn);
		}

		// Light Attenuation:
		bool enableAttenuation = lightAtten > 0.0001f;
		float attenuation = 1.0f;
		if (!isDirectionalLight)	// directional lights do not support attenuation, skip calculation
		{
			attenuation = lerp(1.0, 1 / pow(length(lightVec), lightAtten), enableAttenuation);
		}

		// compensate diffuse and specular color with various light settings:
		specularColor *= (lightColor * lightIntensity * attenuation);
		diffuseColor *= (lightColor * lightIntensity * attenuation);

		// Spot light Cone Angle:
		if (lightType == 2)
		{
			float angle = lightConeangle(lightConeAngle, lightFallOff, lightVec, lightDir);
			diffuseColor *= angle;
			specularColor *= angle;
		}

		// Shadows:
		if (UseShadows && lightShadowOn) 
		{
			float shadow = lightShadow(lightViewPrjMatrix, lightShadowMap, vertWorldPos);
			diffuseColor *= shadow;
			specularColor *= shadow;
		}


		// Translucency should be added on top after shadow and cone:
		if (UseTranslucency)
		{
			float3 transColor = translucency(thickness, eyeVec, L, vertexNormal, attenuation, gammaCorrection, diffuseColorIn);
			diffuseColor += transColor;
		}


		// Add specular and rim light on top of final output color
		// multiply OUT.Color with opacity since we are using a pre-multiplied alpha render state
		// if we don't do this, the rim may have halo's around it when the object is fully transparent
		OUT.Color += diffuseColor;
		OUT.Color *= opacity;
		OUT.Color += specularColor + rimColor;

		// Output specular and rim for opacity:
		OUT.Specular = dot(saturate(specularColor), float3(0.3f, 0.6f, 0.1f)) + rimColor.r;


	} // end if light enabled

	return OUT;
}



//------------------------------------
// vertex shader with tessellation
//------------------------------------
// take inputs from 3d-app
// vertex animation/skinning would happen here
SHADERDATA vt(APPDATA IN) 
{
	SHADERDATA OUT = (SHADERDATA)0;

	// we pass vertices in world space
	OUT.position = mul( float4(IN.position, 1), world );
	OUT.worldPosition.xyz = OUT.position.xyz;

	// Pass through texture coordinates
	// flip Y for Maya
	OUT.texCoord0 = float2(IN.texCoord0.x,(1.0-IN.texCoord0.y));
	OUT.texCoord1 = float2(IN.texCoord1.x,(1.0-IN.texCoord1.y));
	OUT.texCoord2 = float2(IN.texCoord2.x,(1.0-IN.texCoord2.y));

	// output normals in world space:
	OUT.worldNormal = normalize(mul(IN.normal, (float3x3)world));

	// output tangent in world space:
	OUT.worldTangent.xyz = normalize( mul(IN.tangent, (float3x3)world) );

	// store direction for normal map:
	OUT.worldTangent.w = 1;
	if (dot(cross(IN.normal.xyz, IN.tangent.xyz), IN.binormal.xyz) < 0.0) OUT.worldTangent.w = -1;

	return OUT;
}


//------------------------------------
// vertex shader without tessellation
//------------------------------------
SHADERDATA v(APPDATA IN) 
{
	SHADERDATA OUT = vt(IN);
		
	// If we don't use tessellation, pass vertices in clip space:
	OUT.position = mul( float4(OUT.position.xyz, 1), viewPrj );

	return OUT;
}


//------------------------------------
// hull shader
//------------------------------------
// executed once per control point.
// control points can be considered the original vertices of the mesh
// outputs a control point
// run parallel with hull constant function
[domain("tri")]
[partitioning("fractional_odd")]
[outputtopology("triangle_cw")]
[patchconstantfunc("HS_Constant")]
[outputcontrolpoints(3)]
[maxtessfactor(64.0)]


	// PN-AEN without displacement fix:
	// SHADERDATA HS( InputPatch<SHADERDATA, 9> IN, uint index : SV_OutputControlPointID, uint patchID : SV_PrimitiveID )

	// PN Triangles, no crack fixes:
	// SHADERDATA HS( InputPatch<SHADERDATA, 3> IN, uint index : SV_OutputControlPointID, uint patchID : SV_PrimitiveID )


// PN-AEN and displacement fix
//		the index buffer is made up as follows:
//		the triangle vertices index (int3)					// PNAEN9 and PNAEN18
//		the 3 adjacent edges vertices index (3 * int2)		// PNAEN9 and PNAEN18
//		the 3 dominant edges vertices index (3 * int2)		// PNAEN18
//		the dominant position vertices index (int3)			// PNAEN18
SHADERDATA HS( InputPatch<SHADERDATA, 18> IN, uint index : SV_OutputControlPointID, uint patchID : SV_PrimitiveID )
{
	SHADERDATA OUT = (SHADERDATA)0;

	// copy everything first:
	OUT = IN[index];

	// Compute the next output control point ID so we know which edge we're on.
	const uint nextIndex = index < 2 ? index + 1 : 0; // (index + 1) % 3


	// PN-AEN 9 and 18: 
		const uint neighborIndex = 3 + 2 * index;
		const uint neighborNextIndex = neighborIndex + 1;

		float3 myCP, neighborCP;	
	
		// Calculate original PN control points and neighbors'.  Then average.
		myCP = ComputeCP( IN[index].worldPosition, IN[nextIndex].worldPosition, IN[index].worldNormal );
		neighborCP = ComputeCP( IN[neighborIndex].worldPosition, IN[neighborNextIndex].worldPosition, IN[neighborIndex].worldNormal );
		OUT.CP1 = (myCP + neighborCP) / 2;

		myCP = ComputeCP( IN[nextIndex].worldPosition, IN[index].worldPosition, IN[nextIndex].worldNormal );
		neighborCP = ComputeCP( IN[neighborNextIndex].worldPosition, IN[neighborIndex].worldPosition, IN[neighborNextIndex].worldNormal );
		OUT.CP2 = (myCP + neighborCP) / 2;
		
	// PN Triangles only would be:
		// OUT.CP1 = ComputeCP( IN[index].worldPosition, IN[nextIndex].worldPosition, IN[index].worldNormal);
		// OUT.CP2 = ComputeCP( IN[nextIndex].worldPosition, IN[index].worldPosition, IN[nextIndex].worldNormal);

	// Clipping:
		 OUT.clipped = ComputeClipping(OUT.worldPosition, OUT.CP1, OUT.CP2);

	// PN-AEN discontinuity code for displacement UVs:

		const uint dominantEdgeIndex = 9 + 2 * index;
		const uint dominantEdgeNextIndex = dominantEdgeIndex + 1;
		const uint dominantVertexIndex = 15 + index;

		// Note: the order of the vertices/edges we choose here can be different per application and
		//		 depend on how the index buffer was generated.
		//		 These work for Maya with its PN-AEN18 primitive generator
		float2 dominantEdgeUV = pickTexcoord(DisplacementTexcoord, IN[dominantEdgeIndex].texCoord0, IN[dominantEdgeIndex].texCoord1, IN[dominantEdgeIndex].texCoord2);
		float2 dominantEdgeNextUV = pickTexcoord(DisplacementTexcoord, IN[dominantEdgeNextIndex].texCoord0, IN[dominantEdgeNextIndex].texCoord1, IN[dominantEdgeNextIndex].texCoord2);
		float2 dominantVertexUV = pickTexcoord(DisplacementTexcoord, IN[dominantVertexIndex].texCoord0, IN[dominantVertexIndex].texCoord1, IN[dominantVertexIndex].texCoord2);

		OUT.dominantEdge = float4( dominantEdgeNextUV, dominantEdgeUV );
		OUT.dominantVertex = dominantVertexUV;

	// VDM dominant normal and tangent for displacement crack fix:
		OUT.dominantNormalE0 = IN[dominantEdgeNextIndex].worldNormal.xyz;
		OUT.dominantNormalE1 = IN[dominantEdgeIndex].worldNormal.xyz;
		OUT.dominantNormalCorner = IN[dominantVertexIndex].worldNormal.xyz;

		OUT.dominantTangentE0 = IN[dominantEdgeNextIndex].worldTangent.xyz;
		OUT.dominantTangentE1 = IN[dominantEdgeIndex].worldTangent.xyz;
		OUT.dominantTangentCorner = IN[dominantVertexIndex].worldTangent.xyz;

	return OUT;
}


//------------------------------------
// Hull shader constant function
//------------------------------------
// executed once per patch
// outputs user defined data per patch and tessellation factor
// calculates control points for vertex and normal and passes to domain
// This hull shader passes the tessellation factors through to the HW tessellator, 
// run parallel with hull function
HSCONSTANTDATA HS_Constant( const OutputPatch<SHADERDATA, 3> IN, uint patchID : SV_PrimitiveID )
{
	HSCONSTANTDATA OUT = (HSCONSTANTDATA)0;
    
	// future todo:   
	// triangle is on silhouette?
	// triangle is facing camera? If facing backwards, reduce tessellation
	// triangle lies in high frequency area of displacement map (density-based tessellation)?

	// Now setup the PNTriangle control points...
	// Center control point
	float3 f3E = (IN[0].CP1 + IN[0].CP2 + IN[1].CP1 + IN[1].CP2 + IN[2].CP1 + IN[2].CP2) / 6.0f;
	float3 f3V = (IN[0].worldPosition + IN[1].worldPosition + IN[2].worldPosition) / 3.0f;
	OUT.CPCenter = f3E + ((f3E - f3V) / 2.0f);

	// Clipping:
	float4 centerViewPos = mul( float4(OUT.CPCenter, 1), viewPrj );
	bool centerClipped = IsClipped(centerViewPos);

	if (IN[0].clipped && IN[1].clipped && IN[2].clipped && centerClipped) 
	{
        // If all control points are clipped, the surface cannot possibly be visible.
		// Not entirely true, because displacement mapping can make them visible in the domain shader
		// so we provide the user with a bias factor to avoid clipping too early
		OUT.TessFactor[0] = OUT.TessFactor[1] = OUT.TessFactor[2] = 0;
	}
	else
	{
		// Camera based tessellation, per object. So very basic.
		float3 CameraPosition = viewInv[3].xyz;
		float LengthOp = length((CameraPosition - world[3].xyz));
		float DivOp = (TessellationRange / LengthOp);
		float MaxOp = max(TessellationMin + DivOp, 1);
		OUT.TessFactor[0] = OUT.TessFactor[1] = OUT.TessFactor[2] = MaxOp;
	}
 
	// Inside tess factor is just the average of the edge factors
	OUT.InsideTessFactor = ( OUT.TessFactor[0] + OUT.TessFactor[1] + OUT.TessFactor[2] ) / 3.0f;

	return OUT;
}


//------------------------------------
// domain shader
//------------------------------------
// outputs the new vertices based on previous tessellation.
// also calculates new normals and uvs
// This domain shader applies contol point weighting to the barycentric coords produced by the FF tessellator 
// If you wanted to do any vertex lighting, it would have to happen here.
[domain("tri")]
SHADERDATA DS( HSCONSTANTDATA HSIN, OutputPatch<SHADERDATA, 3> IN, float3 f3BarycentricCoords : SV_DomainLocation )
{
	SHADERDATA OUT = (SHADERDATA)0;

	// The barycentric coordinates
	float fU = f3BarycentricCoords.x;
	float fV = f3BarycentricCoords.y;
	float fW = f3BarycentricCoords.z;

	// Precompute squares and squares * 3 
	float fUU = fU * fU;
	float fVV = fV * fV;
	float fWW = fW * fW;
	float fUU3 = fUU * 3.0f;
	float fVV3 = fVV * 3.0f;
	float fWW3 = fWW * 3.0f;

	// PN position:
	float3 position = IN[0].worldPosition * fWW * fW +
						IN[1].worldPosition * fUU * fU +
						IN[2].worldPosition * fVV * fV +
						IN[0].CP1 * fWW3 * fU +
						IN[0].CP2 * fW * fUU3 +
						IN[2].CP2 * fWW3 * fV +
						IN[1].CP1 * fUU3 * fV +
						IN[2].CP1 * fW * fVV3 +
						IN[1].CP2 * fU * fVV3 +
						HSIN.CPCenter * 6.0f * fW * fU * fV;

	// Flat position:
	float3 flatPosition = IN[0].worldPosition * fW +
					IN[1].worldPosition * fU +
					IN[2].worldPosition * fV;

    // allow user to blend between PN tessellation and flat tessellation:
	position = lerp(position, flatPosition, FlatTessellation);

	// Interpolate normal
	float3 normal = IN[0].worldNormal * fW + IN[1].worldNormal * fU + IN[2].worldNormal * fV;

	// Normalize the interpolated normal
	OUT.worldNormal = normalize(normal);

	// Compute tangent:
	float3 tangent = IN[0].worldTangent.xyz * fW + IN[1].worldTangent.xyz * fU + IN[2].worldTangent.xyz * fV;
	OUT.worldTangent.xyz = normalize(tangent.xyz);

	// Pass through the direction of the binormal as calculated in the vertex shader
	OUT.worldTangent.w = IN[0].worldTangent.w;

	// Linear interpolate the texture coords
	OUT.texCoord0 = IN[0].texCoord0 * fW + IN[1].texCoord0 * fU + IN[2].texCoord0 * fV;
	OUT.texCoord1 = IN[0].texCoord1 * fW + IN[1].texCoord1 * fU + IN[2].texCoord1 * fV;
	OUT.texCoord2 = IN[0].texCoord2 * fW + IN[1].texCoord2 * fU + IN[2].texCoord2 * fV;

	// apply displacement map (only when not rendering the Maya preview swatch):
	if (UseDisplacementMap && !IsSwatchRender)
	{
		// Fix Displacement Seams.
		// we assume here that the displacement UVs is UVset 0.
		// if this UVset index is changed, it should als be changed in the hull shader
		// PN-AEN 18 with displacement UV seam fix
		float2 displaceUV = pickTexcoord(DisplacementTexcoord, OUT.texCoord0, OUT.texCoord1, OUT.texCoord2);
		float3 displacementUVW = PickDominant(	float3(displaceUV, 0),
														fU, fV, fW,
														float3( IN[0].dominantEdge.xy, 0), float3( IN[0].dominantEdge.zw, 0), 
														float3( IN[1].dominantEdge.xy, 0), float3( IN[1].dominantEdge.zw, 0),
														float3( IN[2].dominantEdge.xy, 0), float3( IN[2].dominantEdge.zw, 0),
														float3( IN[0].dominantVertex.xy, 0), 
														float3( IN[1].dominantVertex.xy, 0), 
														float3( IN[2].dominantVertex.xy, 0));

		// We can still get cracks here because the world tangent and normal may be different for vertices on each side of the UV seam,
		// because we do the tangent to world conversion, we get the same diplacement amount, but it results in different movement once converted to world space.
		// And even a tiny difference between normal or tangent will cause large cracks.
		float3 displacementNormal = PickDominant(	OUT.worldNormal,
														fU, fV, fW,
														IN[0].dominantNormalE0, IN[0].dominantNormalE1, 
														IN[1].dominantNormalE0, IN[1].dominantNormalE1,
														IN[2].dominantNormalE0, IN[2].dominantNormalE1,
														IN[0].dominantNormalCorner, 
														IN[1].dominantNormalCorner, 
														IN[2].dominantNormalCorner);

		displacementNormal = normalize(displacementNormal);

		if (UseVectorDisplacement)
		{
			float3 displacementTangent = PickDominant(	OUT.worldTangent.xyz,
															fU, fV, fW,
															IN[0].dominantTangentE0, IN[0].dominantTangentE1, 
															IN[1].dominantTangentE0, IN[1].dominantTangentE1,
															IN[2].dominantTangentE0, IN[2].dominantTangentE1,
															IN[0].dominantTangentCorner, 
															IN[1].dominantTangentCorner, 
															IN[2].dominantTangentCorner);

			displacementTangent = normalize(displacementTangent);

			float3 vecDisp = DisplacementTexture.SampleLevel(SamplerAnisoWrap, displacementUVW.xy, 0).xyz;
			vecDisp -= DisplacementOffset;

			float3 Bn = cross(displacementNormal, displacementTangent); 
			float3x3 toWorld = float3x3(displacementTangent, Bn.xyz, displacementNormal);

			float3 VDMcoordSys = vecDisp.xzy;		// Mudbox
			if (VectorDisplacementCoordSys == 1)
			{
				VDMcoordSys = vecDisp.xyz;			// Maya or ZBrush
			}

			float3 vecDispW = mul(VDMcoordSys, toWorld) * DisplacementHeight;
			position.xyz += vecDispW;
		}
		else
		{
			// offset (-0.5) so that we can have negative displacement also
			float offset = DisplacementTexture.SampleLevel(SamplerAnisoClamp, displacementUVW.xy, 0).x - DisplacementOffset;
			position.xyz += displacementNormal * offset * DisplacementHeight;
		}
	}

	// Update World Position value for inside pixel shader:
	OUT.worldPosition = position.xyz;

	// Transform model position with view-projection matrix
	//OUT.position = float4(position.xyz, 1);							// with geo
	OUT.position = mul( float4(position.xyz, 1), viewPrj );				// without geo
        
	return OUT;
}


//------------------------------------
// Geometry Shader
//------------------------------------
// This is a sample Geo shader. Disabled in this shader, but left here for your reference.
// If you wish to enable it, search for 'with geo' in this shader for code to change.
[maxvertexcount(3)] // Declaration for the maximum number of vertices to create
void GS( triangle SHADERDATA IN[3], inout TriangleStream<SHADERDATA> TriStream )
{
	SHADERDATA OUT;
    
	// quick test to see if geo also works:
	for( int i=0; i<3; ++i )
	{
		OUT = IN[i];
		OUT.position = mul( mul( float4(OUT.position.xyz, 1), view) , prj);
		TriStream.Append( OUT );
	}
	TriStream.RestartStrip(); // end triangle
}

//------------------------------------
// pixel shader
//------------------------------------
float4 f(SHADERDATA IN, bool FrontFace : SV_IsFrontFace) : SV_Target
{
	// clip are early as possible
	float2 opacityMaskUV = pickTexcoord(OpacityMaskTexcoord, IN.texCoord0, IN.texCoord1, IN.texCoord2);
	OpacityMaskClip(opacityMaskUV);

	float gammaCorrection = lerp(1.0, 2.2, LinearSpaceLighting);
	
	float3 N = normalize(IN.worldNormal.xyz);
	if (flipBackfaceNormals)
	{
		N = lerp (-N, N, FrontFace);
	}
	float3 Nw = N;


	if (UseNormalTexture)
	{
		float3 T = normalize(IN.worldTangent.xyz);
		float3 Bn = cross(N, T); 
		Bn *= IN.worldTangent.w; 
		float3x3 toWorld = float3x3(T, Bn, N);

		float2 normalUV = pickTexcoord(NormalTexcoord, IN.texCoord0, IN.texCoord1, IN.texCoord2);
		float3 NormalMap = NormalTexture.Sample(SamplerAnisoWrap, normalUV).xyz * 2 - 1;

		NormalMap.xy *= NormalHeight; 
		NormalMap = mul(NormalMap.xyz, toWorld);
		N = normalize(NormalMap.rgb);
	}
	
	float3 V = normalize( viewInv[3].xyz - IN.worldPosition.xyz );

	float glossiness =  max(1.0, SpecPower);
	float specularAlpha = 1.0;
	float3 specularColor = SpecularColor;
	if (UseSpecularTexture)
	{
		float2 opacityUV = pickTexcoord(SpecularTexcoord, IN.texCoord0, IN.texCoord1, IN.texCoord2);
		float4 SpecularTextureSample = SpecularTexture.Sample(SamplerAnisoWrap, opacityUV);

		specularColor *= pow(SpecularTextureSample.rgb, gammaCorrection);
		specularAlpha = SpecularTextureSample.a;
		glossiness *= (SpecularTextureSample.a + 1);
	}

	float roughness = min( SpecPower/100.0f, 1) * specularAlpha;		// divide by 100 so we get more user friendly values when switching from Phong based on slider range.
	roughness = 1.0f-roughness;											// flip so it is more user friendly when switching from Phong

	float fresnel = saturate((saturate(1.0f - dot(N, V))-ReflectionFresnelMin)/(ReflectionFresnelMax - ReflectionFresnelMin));	

	float3 ReflectionColor = lerp(float3(1,1,1), specularColor, UseSpecColorToTintReflection) * (ReflectionIntensity*UseCubeMap) * fresnel;	
	if (UseReflectionMask)
	{
		float2 reflectionMaskUV = pickTexcoord(ReflectionMaskTexcoord, IN.texCoord0, IN.texCoord1, IN.texCoord2);
		float4 ReflectionMaskSample = ReflectionMask.Sample(SamplerAnisoWrap, reflectionMaskUV);

		ReflectionColor *=  ReflectionMaskSample.r;
	}

	float3 CubeMap = ReflectionColor;
	if (UseCubeMap)
	{
		float3 ReflectionVector = reflect(-V, N);
		// below "8" should really be the number of mip maps levels in the cubemap, but since we don't know this (Maya is not passing this to us) we guess hard code it.
		float ReflectionMipLevel = (ReflectionBlur + (8.0 * (UseSpecAlphaForReflectionBlur * (1 - specularAlpha))));
		CubeMap *= pow(CubeMapTexture.SampleLevel(CubeMapSampler, ReflectionVector, ReflectionMipLevel).rgb, gammaCorrection);	
	}
	
	float3 diffuseColor = DiffuseColor;
	diffuseColor *= (1 - saturate(ReflectionColor));
	float DiffuseAlpha = 1.0f;
	if (UseDiffuseTexture)
	{
		float2 diffuseUV = pickTexcoord(DiffuseTexcoord, IN.texCoord0, IN.texCoord1, IN.texCoord2);
		float4 DiffuseTextureSample = DiffuseTexture.Sample(SamplerAnisoWrap, diffuseUV);

		if (UseDiffuseTextureAlpha)
		{
			DiffuseAlpha = DiffuseTextureSample.a;
		}
		diffuseColor *= pow(DiffuseTextureSample.rgb, gammaCorrection);
	}

	if (UseLightmapTexture)
	{
		// if this was a AO map, we would want to apply it to the ambient, but we do not consider this a AO map at this time
		// We assume this texture does not need to be converted to linear space
		float2 lightmapUV = pickTexcoord(LightmapTexcoord, IN.texCoord0, IN.texCoord1, IN.texCoord2);
		float4 LightmapTextureSample = LightmapTexture.Sample(SamplerAnisoWrap, lightmapUV);

		diffuseColor *= LightmapTextureSample.rgb; // pow(LightmapTextureSample.rgb, gammaCorrection);
	}

	float3 AmbientColor = (lerp(AmbientGroundColor, AmbientSkyColor, ((N.y * 0.5) + 0.5)) * diffuseColor);
	if (UseEmissiveTexture)
	{
		float2 emissiveUV = pickTexcoord(EmissiveTexcoord, IN.texCoord0, IN.texCoord1, IN.texCoord2);
		float4 EmissiveColor = EmissiveTexture.Sample(SamplerAnisoWrap, emissiveUV);

		AmbientColor += EmissiveColor.rgb;
	}


	float3 thickness = float3(1,1,1);
	if (UseThicknessTexture)
	{
		float2 thicknessUV = pickTexcoord(ThicknessTexcoord, IN.texCoord0, IN.texCoord1, IN.texCoord2);
		thickness = TranslucencyThicknessMask.Sample(SamplerAnisoWrap, thicknessUV).xyz;
	}

	float softenMask = 1.0f;
	if (UseSoftenDiffuseTexture)
	{
		float2 softenUV = pickTexcoord(SoftenDiffuseMaskTexcoord, IN.texCoord0, IN.texCoord1, IN.texCoord2);
		softenMask = SoftenDiffuseMask.Sample(SamplerAnisoWrap, softenUV).r;
	}

	float rim = saturate((saturate(1.0f - dot(N, V))-rimFresnelMin)/(max(rimFresnelMax, rimFresnelMin)  - rimFresnelMin));
	rim *= rimBrightness * max(specularAlpha, 0.2);	

	float opacity = (DiffuseAlpha * Opacity);


	// --------
	// LIGHTS:
	// --------
	// future todo: Maya could pass light info in array so we can loop any number of lights.

	// light 0:
	lightOut light0 = CalculateLight(	light0Enable, light0Type, light0AttenScale, light0Pos, IN.worldPosition.xyz, 
										light0Color, light0Intensity, light0Dir, light0ConeAngle, light0FallOff, light0Matrix, 
										light0ShadowMap, light0ShadowOn, Nw, N, diffuseColor, V, roughness, specularColor,
										thickness, softenMask, gammaCorrection, rim, glossiness, opacity );

	// light 1:
	lightOut light1 = CalculateLight(	light1Enable, light1Type, light1AttenScale, light1Pos, IN.worldPosition.xyz, 
										light1Color, light1Intensity, light1Dir, light1ConeAngle, light1FallOff, light1Matrix, 
										light1ShadowMap, light1ShadowOn, Nw, N, diffuseColor, V, roughness, specularColor,
										thickness, softenMask, gammaCorrection, rim, glossiness, opacity );

	// light 2:
	lightOut light2 = CalculateLight(	light2Enable, light2Type, light2AttenScale, light2Pos, IN.worldPosition.xyz, 
										light2Color, light2Intensity, light2Dir, light2ConeAngle, light2FallOff, light2Matrix, 
										light2ShadowMap, light2ShadowOn, Nw, N, diffuseColor, V, roughness, specularColor,
										thickness, softenMask, gammaCorrection, rim, glossiness, opacity );


	// final color:
	// ambient must also compensate for pre-multiplied alpha
	float3 result = (AmbientColor * opacity) + CubeMap;
	result += light0.Color + light1.Color + light2.Color;
	result = pow(result, 1/gammaCorrection);

	// final alpha:
	float cubeTransparency = dot(saturate(CubeMap), float3(0.3, 0.6, 0.1));
	float specTotal = light0.Specular + light1.Specular + light2.Specular;
	float transparency = (cubeTransparency + specTotal) + opacity;
	transparency = saturate(transparency);	// keep 0-1 range

	return float4(result, transparency);
}


//------------------------------------
// wireframe pixel shader
//------------------------------------
float4 fwire(SHADERDATA IN) : SV_Target
{
	return float4(0,0,1,1);
}


//------------------------------------
// pixel shader for shadow map generation
//------------------------------------
//float4 ShadowMapPS( float3 Pw, float4x4 shadowViewProj ) 
float4 ShadowMapPS(SHADERDATA IN) : SV_Target
{ 
	// clip as early as possible
	float2 opacityMaskUV = pickTexcoord(OpacityMaskTexcoord, IN.texCoord0, IN.texCoord1, IN.texCoord2);
	OpacityMaskClip(opacityMaskUV);

	float4 Pndc = mul( float4(IN.worldPosition, 1.0f), viewPrj ); 

	// divide Z and W component from clip space vertex position to get final depth per pixel
	float retZ = Pndc.z / Pndc.w; 

	retZ += fwidth(retZ); 
	return retZ.xxxx; 
} 

//-----------------------------------
// Objects without tessellation
//------------------------------------
technique11 TessellationOFF
<
	bool overridesDrawState = false;	// we do not supply our own render state settings
	int isTransparent = 3;
	// objects with clipped pixels need to be flagged as isTransparent to avoid the occluding underlying geometry since Maya renders the object with flat shading when computing depth
	string transparencyTest = "Opacity < 1.0 || (UseDiffuseTexture && UseDiffuseTextureAlpha) || UseOpacityMaskTexture";
	bool VariableNameAsAttributeName = false;	// keep old variable names for this old shader for backwards compatibility
>
{  
	pass p0
	< 
		string drawContext = "colorPass";	// tell maya during what draw context this shader should be active, in this case 'Color'
	>
	{
		// even though overrideDrawState is false, we still set the pre-multiplied alpha state here in
		// case Maya is using 'Depth Peeling' transparency algorithm
		// This unfortunately won't solve sorting issues, but at least our object can draw transparent.
		// If we don't set this, the object will always be opaque.
		// In the future, hopefully ShaderOverride nodes can participate properly in Maya's Depth Peeling setup
		SetBlendState(PMAlphaBlending, float4(0.0f, 0.0f, 0.0f, 0.0f), 0xFFFFFFFF);
		SetVertexShader(CompileShader(vs_5_0, v()));
		SetHullShader(NULL);
		SetDomainShader(NULL);
		SetGeometryShader(NULL);
		SetPixelShader(CompileShader(ps_5_0, f()));
	}

	pass pShadow
	< 
		string drawContext = "shadowPass";	// shadow pass
	>
	{
		SetVertexShader(CompileShader(vs_5_0, v()));
		SetHullShader(NULL);
		SetDomainShader(NULL);
		SetGeometryShader(NULL);
		SetPixelShader(CompileShader(ps_5_0, ShadowMapPS()));
	}
}

//-----------------------------------
// Objects with tessellation
//------------------------------------
// Vertex Index Buffer options:
// index_buffer_type: None;			// no divergent normals and no displacement crack fix
// index_buffer_type: PNAEN9;		// divergent normals crack fix; no displacement UV seam crack fix
// index_buffer_type: PNAEN18,		// crack fix for divergent normals and UV seam displacement
technique11 TessellationON
<
	string index_buffer_type = "PNAEN18";	// tell Maya what type of index buffer we want. Must be unique name per generator
	bool overridesDrawState = false;
	int isTransparent = 3;
	string transparencyTest = "Opacity < 1.0 || (UseDiffuseTexture && UseDiffuseTextureAlpha) || UseOpacityMaskTexture";
	bool VariableNameAsAttributeName = false;	// keep old variable names for this old shader for backwards compatibility
>
{  
	pass p0
	< 
		string drawContext = "colorPass";
	>
	{
		SetBlendState(PMAlphaBlending, float4(0.0f, 0.0f, 0.0f, 0.0f), 0xFFFFFFFF);
		SetVertexShader(CompileShader(vs_5_0, vt()));
		SetHullShader(CompileShader(hs_5_0, HS()));
		SetDomainShader(CompileShader(ds_5_0, DS()));
		SetGeometryShader(NULL);								// without geo
		//SetGeometryShader( CompileShader(gs_5_0, GS()) );		// with geo
		SetPixelShader(CompileShader(ps_5_0, f()));
	}

	pass pShadow
	< 
		string drawContext = "shadowPass";	// shadow pass
	>
	{
		SetVertexShader(CompileShader(vs_5_0, vt()));
		SetHullShader(CompileShader(hs_5_0, HS()));
		SetDomainShader(CompileShader(ds_5_0, DS()));
		SetGeometryShader(NULL);
		SetPixelShader(CompileShader(ps_5_0, ShadowMapPS()));
	}
}

//-----------------------------------
// Wireframe
//------------------------------------
technique11 WireFrame
<
	string index_buffer_type = "PNAEN18";
	bool overridesDrawState = false;		// since we only change the fillMode, it can remain on false. If we changed the blend state, it would have to be true
	int isTransparent = 0;
	bool VariableNameAsAttributeName = false;	// keep old variable names for this old shader for backwards compatibility
>
{  
	pass p0
	< 
		string drawContext = "colorPass";
	>
	{
		SetRasterizerState(WireframeCullFront);
		SetVertexShader(CompileShader(vs_5_0, vt()));
		SetHullShader(CompileShader(hs_5_0, HS()));
		SetDomainShader(CompileShader(ds_5_0, DS()));
		SetGeometryShader(NULL);								// without geo
		//SetGeometryShader( CompileShader(gs_5_0, GS()) );		// with geo
		SetPixelShader(CompileShader(ps_5_0, fwire()));
	}
}

