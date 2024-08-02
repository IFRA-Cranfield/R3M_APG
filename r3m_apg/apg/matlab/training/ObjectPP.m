%% Create Environment
clc
clear
close all

mdl='ObjectPP';
open_system(mdl)

obsInfo = rlNumericSpec([4 1],...
    LowerLimit=[0 1 0 0]',...
    UpperLimit=[100 5 1 1]');
obsInfo.Name = "Observations";

actInfo = rlFiniteSetSpec([01 02 03 04 05 06 07]);
actInfo.Name = "Control Action";

env = rlSimulinkEnv(mdl, [mdl '/RL Agent'],...
    obsInfo,actInfo);

%% Create DQN Agent

nI = obsInfo.Dimension(1);  % number of inputs (6)
nL = 300;                            % number of neurons
nO = numel(actInfo.Elements);    % number of outputs (31)

dnn = [
    featureInputLayer(nI,'Normalization','none','Name','state')
    fullyConnectedLayer(nL,'Name','fc1')
    reluLayer('Name','relu1')
    fullyConnectedLayer(nL,'Name','fc2')
    reluLayer('Name','relu2')
    fullyConnectedLayer(nO,'Name','fc3')];
dnn = dlnetwork(dnn);

criticOptions = rlOptimizerOptions('LearnRate',1e-2,'GradientThreshold',1,'L2RegularizationFactor',1e-3);

critic = rlVectorQValueFunction(dnn,obsInfo,actInfo);

agentOptions = rlDQNAgentOptions(...
    'UseDoubleDQN',true,...
    'CriticOptimizerOptions',criticOptions,...
    'ExperienceBufferLength',1e4,...
    'MiniBatchSize',64,...
    'TargetSmoothFactor',1e-3,...
    'TargetUpdateFrequency',1,...
    'NumStepsToLookAhead',1);

agentOptions.EpsilonGreedyExploration.Epsilon = 1;
agentOptions.EpsilonGreedyExploration.EpsilonDecay = 0.001;
agentOptions.EpsilonGreedyExploration.EpsilonMin = 0.01;

agent = rlDQNAgent(critic,agentOptions);

maxepisodes = 5000;
maxsteps = 10;
trainOpts = rlTrainingOptions(...
    'MaxEpisodes',maxepisodes, ...
    'MaxStepsPerEpisode',maxsteps, ...
    'ScoreAveragingWindowLength',5, ...
    'Verbose',false, ...
    'Plots','training-progress',...
    'StopTrainingCriteria','AverageReward',...
    'StopTrainingValue',4500);

doTraining = true;

if doTraining    
    % Train the agent.
    %saveDir = 'savedAgents';
    %cd(saveDir);
    %load('Tt02.mat','agent');
    %cd ..
    trainingStats = train(agent,env,trainOpts);
else
    % Load the pretrained agent for the example.
    load('SimulinkLKADQNMulti.mat','agent')       
end

%% SAVE AGENT

%reset(agent); % Clears the experience buffer
saveDir = 'savedAgents';
cd(saveDir)
save('Tt02','agent');
cd ..

%% Generate Code

saveDir = 'savedAgents';
cd(saveDir)
load('Agent01.mat','agent')
%cd ..\

generatePolicyFunction(agent)

cfg = coder.gpuConfig('mex');
cfg.TargetLang = 'C++';
cfg.DeepLearningConfig = coder.DeepLearningConfig('cudnn');

argstr = '{ones(14,1)}';

codegen('-config','cfg','evaluatePolicy','-args',argstr,'-report');