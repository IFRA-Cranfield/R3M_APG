function action1 = evaluatePolicy(observation1, AGENT)
%#codegen

% Reinforcement Learning Toolbox
% Generated on: 01-Mar-2024 17:28:49

persistent policy;
if isempty(policy)
	policy = coder.loadRLPolicy(AGENT);
end
% evaluate the policy
action1 = getAction(policy,observation1);