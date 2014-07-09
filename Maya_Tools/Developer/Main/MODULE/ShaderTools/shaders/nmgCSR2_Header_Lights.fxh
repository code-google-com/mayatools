////////////////////////////////////////
//     Lights - position and color    //
////////////////////////////////////////
//bool spacerLights<string UIName   = "******************************************";> = false;
//bool spacerLights1<string UIName   = "***** + (3 DIRECTIONAL LIGHTS) *****";> = false;
float4 light1Dir : DIRECTION
<
  string UIName = "Light 1 - Directional Light";
  string Space  = "World";
> = {0.0, -1.0, -1.0, 0.0};

float3 light1Color
<
  string UIName   = "Light1Color";
  string Type     = "Color";
> = {1.0, 1.0, 1.0};

//bool spacerLights2<string UIName   = ">>>>>>>>>>>>>>>>>>>>>>>>>>";> = false;
float4 light2Dir : DIRECTION
<
  string UIName = "Light 2 - Directional Light";
  string Space  = "World";
> = {-1.0, 1.0, 1.0, 0.0};

float3 light2Color
<
  string UIName   = "Light2Color";
  string Type     = "Color";
> = {0.00, 0.00, 0.00};

//bool spacerLights3<string UIName   = ">>>>>>>>>>>>>>>>>>>>>>>>>>";> = false;
float4 light3Dir : DIRECTION
<
  string UIName = "Light 3 - Directional Light";
  string Space  = "World";
> = {-1.0, 1.0, 1.0, 0.0};

float3 light3Color
<
  string UIName   = "Light3Color";
  string Type     = "Color";
> = {0.00, 0.00, 0.00};

//bool spacerLights4<string UIName   = "***** + (3 POINT LIGHTS) *****";> = false;
float4 light4Pos : POSITION
<
  string UIName = "Light 4 - Point Light";
  string Object = "PointLight";
  string Space  = "World";
> = {0.0, 0.0, 0.0, 0.0};

float3 light4Color
<
  string UIName   = "Light4Color";
  string Type     = "Color";
> = { 0.00, 0.00, 0.00};

float light4atten
<
  float UIMin = 0.0;
  float UIMax = 10000.0;
  float UIStep = 0.1;
  string UIName = "Light 4 Attenuation";
> = 1.0;

//bool spacerLights5<string UIName   = ">>>>>>>>>>>>>>>>>>>>>>>>>>";> = false;
float4 light5Pos : POSITION
<
  string UIName = "Light 5 - Point Light";
  string Object = "PointLight";
  string Space  = "World";
> = {0.0, 0.0, 0.0, 0.0};

float3 light5Color
<
  string UIName   = "Light5Color";
  string Type     = "Color";
> = { 0.00, 0.00, 0.00};

float light5atten
<
  float UIMin = 0.0;
  float UIMax = 10000.0;
  float UIStep = 0.1;
  string UIName = "Light 5 Attenuation";
> = 1.0;

//bool spacerLights6<string UIName   = ">>>>>>>>>>>>>>>>>>>>>>>>>>";> = false;
float4 light6Pos : POSITION
<
  string UIName = "Light 6 - Point Light";
  string Object = "PointLight";
  string Space  = "World";
> = {0.0, 0.0, 0.0, 0.0};

float3 light6Color
<
  string UIName   = "Light6Color";
  string Type     = "Color";
> = { 0.00, 0.00, 0.00};

float light6atten
<
  float UIMin = 0.0;
  float UIMax = 10000.0;
  float UIStep = 0.1;
  string UIName = "Light 6 Attenuation";
> = 1.0;