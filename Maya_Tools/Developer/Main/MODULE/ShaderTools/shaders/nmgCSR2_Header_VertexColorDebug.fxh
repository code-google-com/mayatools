float4 PS_DebugVertColor (vert2pixel IN, uniform int whatChannel) : COLOR
{  
  float3 AO = IN.vertColor;
  
  float3 Ci = 0;  //Incident Color
  float Oi = 1.0;
  
  if (whatChannel == 0) // Red
	Ci = float3 (AO.r, AO.r, AO.r);
  else if (whatChannel == 1) { // Green
    //if (AO.g != AO.r)
	//	Ci = float3 (1, AO.g, 1);
	//else
	//	Ci = float3 (AO.g, AO.g, AO.g);
	Ci = float3 (AO.g, AO.g, AO.g);
  }
  else if (whatChannel == 2) {// Blue
    Ci = float3 (AO.b, AO.b, AO.b);
  }
  else if (whatChannel == -1) // All
    Ci = float3 (AO.r, AO.g, AO.b);

  return float4(Ci,Oi);  //Incident Color and Incident Opacity
}
technique Debug_VertColorRed
{
  pass Front
  {
    CullFaceEnable=true;
    CullMode = Back;
    VertexProgram   = compile vp40 VS(false);
    FragmentProgram = compile fp40 PS_DebugVertColor(0);
  }
}
technique Debug_VertColorGreen
{
  pass Front
  {
    CullFaceEnable=true;
    CullMode = Back;
    VertexProgram   = compile vp40 VS(false);
    FragmentProgram = compile fp40 PS_DebugVertColor(1);
  }
}
technique Debug_VertColorBlue
{
  pass Front
  {
    CullFaceEnable=true;
    CullMode = Back;
    VertexProgram   = compile vp40 VS(false);
    FragmentProgram = compile fp40 PS_DebugVertColor(2);
  }
}