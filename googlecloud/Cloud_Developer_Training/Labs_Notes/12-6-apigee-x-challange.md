After failing at this 2 times ( 6+ hours )

This was the way ( I had many errors in my stuff )
https://github.com/Itsabhishek7py/GoogleCloudSkillsboost/blob/main/Develop%20and%20Secure%20APIs%20with%20Apigee%20X%20Challenge%20Lab/lab.md

- Confirm that the cloud's 'Translation API' is enabled


apigee-proxy@qwiklabs-gcp-03-0ea99d8cca96.iam.gserviceaccount.com


TEST_VM_ZONE=$(gcloud compute instances list --filter="name=('apigeex-test-vm')" --format "value(zone)")
gcloud compute ssh apigeex-test-vm --zone=${TEST_VM_ZONE} --force-key-file-overwrite

export API_KEY=$(gcloud auth print-access-token)
curl -i -k -X POST "https://eval.example.com/translate/v1" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ${API_KEY}" \
     -d '{ "q": "Translate this text!", "target": "es" }'

curl -i -k -X GET "https://eval.example.com/translate/v1/languages" -H "Content-Type: application/json" \
     -H "Authorization: Bearer ${API_KEY}" \

curl -i -k -X POST "https://eval.example.com/translate/v1?lang=de" -H "Content-Type:application/json"  -H "Authorization: Bearer ${API_KEY}" -d '{ "text": "Hello world!" }' 

translate-app key
Hd7UUFaUGNfGeGRdr4WopC2njPcuWWfEEEf1LAG73bGLXnU2

Broken: BuildTranslateRequest

AM-BuildErrorResponse

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<AssignMessage async="false" continueOnError="false" enabled="true" name="AM-BuildErrorResponse">
  <DisplayName>AM-BuildErrorResponse</DisplayName>
  <Properties/>
  <Set>
    <Payload contentType="application/json">{ "error": "Invalid request. Verify the lang query parameter." }</Payload>
    <StatusCode>400</StatusCode>
    <ReasonPhrase>Bad Request</ReasonPhrase>
  </Set>
  <!-- By default, AssignMessage in a FaultRule assigns to the ambient message,
         which is the response message in this context. No need for <AssignTo>. -->
</AssignMessage>

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<AssignMessage name="AM-BuildLanguagesRequest">
  <Set>
    <Verb>POST</Verb>
    <!-- Change verb to POST for the backend -->
    <Payload type="application/json">{
            "target": "{properties.language.caller}"
        }</Payload>
    <Headers>
      <Header name="Content-Type">application/json</Header>
    </Headers>
  </Set>
  <AssignTo createNew="true" type="request">backendRequest</AssignTo>
  <!-- The createNew="true" here means you are creating a new request message
         variable (e.g., 'backendRequest') which you would then reference
         in a ServiceCallout policy to send to the backend. -->
</AssignMessage>

Broken: BuildTranslateRequest

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<AssignMessage async="false" continueOnError="false" enabled="true" name="AM-BuildTranslateRequest">
  <DisplayName>AM-BuildTranslateRequest</DisplayName>
  <Properties/>
  <AssignVariable>
    <Name>text</Name>
    <Template>{jsonPath(request.content, '$.text')}</Template>
    $.data.translations[0].translatedText 
  </AssignVariable>
  <AssignVariable>
    <Name>language</Name>
    <Value>{firstnonnull(request.queryparam.lang, language.output)}</Value>
    properties.language.output
     properties.language.properties.output
     language.properties.output
     language.output
  </AssignVariable>
  <Set>
    <Payload type="application/json">{
            "q": "{text}",
            "target": "{language}"
        }</Payload>
  </Set>
  <AssignTo createNew="true" transport="http" type="request"/>
</AssignMessage>


<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<AssignMessage name="AM-BuildTranslateResponse">
  <AssignVariable>
    <Name>translated</Name>
    <Ref>jsonPath(response.content, '$.data.translations[0].translatedText')</Ref>
  </AssignVariable>
  <Set>
    <Payload type="application/json">{
            "translatedText": "{translated}"
        }</Payload>
  </Set>
  <AssignTo createNew="true" type="response"/>
  <!-- This creates a brand new response message -->
</AssignMessage>

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ExtractVariables name="EV-ExtractRequest">
  <Source>request</Source>
  <JSONPayload>
    <Variable name="output">
      <JSONPath>$.output</JSONPath>
    </Variable>
    <Variable name="caller">
      <JSONPath>$.caller</JSONPath>
    </Variable>
  </JSONPayload>
  <IgnoreUnresolvedVariables>false</IgnoreUnresolvedVariables>
</ExtractVariables>

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Javascript continueOnError="false" enabled="true" timeLimit="200" name="JS-BuildLanguagesResponse">
  <DisplayName>JS-BuildLanguagesResponse</DisplayName>
  <Properties/>
  <ResourceURL>jsc://languageresponse.js</ResourceURL>
</Javascript>
reasources
var responseContent = context.getVariable('response.content');
if (responseContent) {
    var responseJson = JSON.parse(responseContent);
    if (responseJson.data && responseJson.data.languages) {
        var languagesJson = JSON.stringify(responseJson.data.languages);
        context.setVariable('response.content', languagesJson);
    } else {
        // Handle case where data.languages is not found, perhaps log an error
        context.setVariable('response.content', JSON.stringify({ error: "Languages data not found in backend response" }));
        context.setVariable('error.state', 'true'); // Or a custom error variable
    }
} else {
    // Handle case where response.content is empty
    context.setVariable('response.content', JSON.stringify({ error: "Empty backend response" }));
    context.setVariable('error.state', 'true');
}

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<MessageLogging async="true" continueOnError="true" enabled="true" name="ML-LogTranslation">
  <DisplayName>ML-LogTranslation</DisplayName>
  <CloudLogging>
    <LogName>projects/{organization.name}/logs/translate</LogName>
    <Message contentType="text/plain">{language}|{text}|{translated}</Message>
  </CloudLogging>
</MessageLogging>

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Quota continueOnError="false" enabled="true" name="Q-EnforceQuota" type="calendar">
  <DisplayName>Q-EnforceQuota</DisplayName>
  <Properties/>
  <Distributed>true</Distributed>
  <Synchronous>true</Synchronous>
  <StartTime>2013-08-21 10:00:00</StartTime>
  <UseQuotaConfigInAPIProduct stepName="VA-VerifyKey">
    <DefaultConfig>
      <Allow>10</Allow>
      <Interval>1</Interval>
      <TimeUnit>minute</TimeUnit>
    </DefaultConfig>
  </UseQuotaConfigInAPIProduct>
</Quota>

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<VerifyAPIKey async="false" continueOnError="false" enabled="true" name="VA-VerifyKey">
  <DisplayName>VA-VerifyKey</DisplayName>
  <APIKey ref="request.header.apikey"/>
</VerifyAPIKey>


resources / properties / language.properties
language.properties
output=es, caller=en