%% General RCbenchmark Motor-Log Plotter
% Prompts for motor and propeller descriptions.
% Creates separate figures for each measured quantity.
% Plot titles and annotations use LaTeX formatting.

clear;
clc;
close all;

%% Global formatting
set(groot, 'defaultTextInterpreter', 'latex');
set(groot, 'defaultAxesTickLabelInterpreter', 'latex');
set(groot, 'defaultLegendInterpreter', 'latex');

markerSize   = 10;
fontSize     = 16;
titleSize    = 22;
subtitleSize = 11;

%% Prompt for test description
answer = inputdlg( ...
    {'Motor description:', 'Propeller description:'}, ...
    'Motor Test Description', ...
    [1 60; 1 60], ...
    {'T-Motor MN3110 700 KV', 'APC 11x7E'});

if isempty(answer)
    disp('Input cancelled.');
    return;
end

motorDescription = strtrim(answer{1});
propDescription  = strtrim(answer{2});

motorLatex = escapeLatex(motorDescription);
propLatex  = escapeLatex(propDescription);

subtitleText = sprintf( ...
    '$\\mathrm{Motor:~%s \\qquad Propeller:~%s}$', ...
    motorLatex, propLatex);

%% Select CSV file
[fileName, filePath] = uigetfile( ...
    {'*.csv', 'CSV files (*.csv)'}, ...
    'Select RCbenchmark Motor Log');

if isequal(fileName, 0)
    disp('No file selected.');
    return;
end

dataFile = fullfile(filePath, fileName);

%% Load data
T = readtable(dataFile, 'VariableNamingRule', 'preserve');

fprintf('Loaded: %s\n', dataFile);
fprintf('Samples: %d\n', height(T));
fprintf('Motor: %s\n', motorDescription);
fprintf('Propeller: %s\n\n', propDescription);

%% Detect columns
timeName = findColumn(T, { ...
    'Time (s)', ...
    'Time'});

escName = findColumn(T, { ...
    'ESC signal (µs)', ...
    'ESC Signal (µs)', ...
    'ESC signal (us)', ...
    'ESC Signal (us)'});

thrustName = findColumn(T, { ...
    'Thrust (kgf)', ...
    'Thrust (kg)'});

currentName = findColumn(T, { ...
    'Current (A)', ...
    'Motor Current (A)'});

rpmName = findColumn(T, { ...
    'Motor Electrical Speed (RPM)', ...
    'Motor Optical Speed (RPM)', ...
    'Motor Speed (RPM)', ...
    'RPM'});

efficiencyName = findColumn(T, { ...
    'Overall Efficiency (kgf/W)', ...
    'Overall Efficiency (g/W)', ...
    'Efficiency (kgf/W)', ...
    'Efficiency (g/W)'});

%% Require ESC command
if isempty(escName)
    error('No ESC signal column was found.');
end

esc = T.(escName);

%% ========================================================================
% ESC Command vs Time
% =========================================================================
if ~isempty(timeName)

    time = T.(timeName);
    idx = isfinite(time) & isfinite(esc);

    figure('Color','w','Name','ESC Signal vs Time');

    scatter(time(idx), esc(idx), markerSize, 'filled');

    grid on;
    box on;

    ax = gca;

    xlabel( ...
        '$t\;(\mathrm{s})$', ...
        'Interpreter','latex', ...
        'FontSize',fontSize);

    ylabel( ...
        '$\mathrm{ESC\ Command\ Pulse\ Width}\;(\mu\mathrm{s})$', ...
        'Interpreter','latex', ...
        'FontSize',fontSize);

    set(ax, ...
        'FontSize',fontSize, ...
        'TickLabelInterpreter','latex');

    addPlotTitles( ...
        ax, ...
        '$\mathrm{ESC\ Command\ Pulse\ Width\ vs.\ Time}$', ...
        subtitleText, ...
        titleSize, ...
        subtitleSize);
end

%% ========================================================================
% Thrust vs ESC Command
% =========================================================================
if ~isempty(thrustName)

    thrust = T.(thrustName);
    idx = isfinite(esc) & isfinite(thrust);

    figure('Color','w','Name','Thrust vs ESC Signal');

    scatter(esc(idx), thrust(idx), markerSize, 'filled');

    grid on;
    box on;

    ax = gca;

    xlabel( ...
        '$\mathrm{ESC\ Command\ Pulse\ Width}\;(\mu\mathrm{s})$', ...
        'Interpreter','latex', ...
        'FontSize',fontSize);

    ylabel( ...
        '$T\;(\mathrm{kg_f})$', ...
        'Interpreter','latex', ...
        'FontSize',fontSize);

    set(ax, ...
        'FontSize',fontSize, ...
        'TickLabelInterpreter','latex');

    addPlotTitles( ...
        ax, ...
        '$\mathrm{Static\ Thrust\ vs.\ ESC\ Command}$', ...
        subtitleText, ...
        titleSize, ...
        subtitleSize);
end

%% ========================================================================
% Current vs ESC Command
% =========================================================================
if ~isempty(currentName)

    current = T.(currentName);
    idx = isfinite(esc) & isfinite(current);

    figure('Color','w','Name','Current vs ESC Signal');

    scatter(esc(idx), current(idx), markerSize, 'filled');

    grid on;
    box on;

    ax = gca;

    xlabel( ...
        '$\mathrm{ESC\ Command\ Pulse\ Width}\;(\mu\mathrm{s})$', ...
        'Interpreter','latex', ...
        'FontSize',fontSize);

    ylabel( ...
        '$I\;(\mathrm{A})$', ...
        'Interpreter','latex', ...
        'FontSize',fontSize);

    set(ax, ...
        'FontSize',fontSize, ...
        'TickLabelInterpreter','latex');

    addPlotTitles( ...
        ax, ...
        '$\mathrm{Motor\ Current\ vs.\ ESC\ Command}$', ...
        subtitleText, ...
        titleSize, ...
        subtitleSize);
end

%% ========================================================================
% RPM vs ESC Command
% =========================================================================
if ~isempty(rpmName)

    rpm = T.(rpmName);
    idx = isfinite(esc) & isfinite(rpm);

    figure('Color','w','Name','RPM vs ESC Signal');

    scatter(esc(idx), rpm(idx), markerSize, 'filled');

    grid on;
    box on;

    ax = gca;

    xlabel( ...
        '$\mathrm{ESC\ Command\ Pulse\ Width}\;(\mu\mathrm{s})$', ...
        'Interpreter','latex', ...
        'FontSize',fontSize);

    ylabel( ...
        '$n\;(\mathrm{RPM})$', ...
        'Interpreter','latex', ...
        'FontSize',fontSize);

    set(ax, ...
        'FontSize',fontSize, ...
        'TickLabelInterpreter','latex');

    addPlotTitles( ...
        ax, ...
        '$\mathrm{Motor\ Speed\ vs.\ ESC\ Command}$', ...
        subtitleText, ...
        titleSize, ...
        subtitleSize);
end

%% ========================================================================
% Thrust Efficiency vs ESC Command
% =========================================================================
if ~isempty(efficiencyName)

    efficiency = T.(efficiencyName);
    idx = isfinite(esc) & isfinite(efficiency);

    figure('Color','w','Name','Efficiency vs ESC Signal');

    scatter(esc(idx), efficiency(idx), markerSize, 'filled');

    grid on;
    box on;

    ax = gca;

    xlabel( ...
        '$\mathrm{ESC\ Command\ Pulse\ Width}\;(\mu\mathrm{s})$', ...
        'Interpreter','latex', ...
        'FontSize',fontSize);

    if contains(efficiencyName,'g/W') && ...
            ~contains(efficiencyName,'kgf/W')

        effLabel = ...
            '$T/P_{\mathrm{elec}}\;(\mathrm{g/W})$';

    else

        effLabel = ...
            '$T/P_{\mathrm{elec}}\;(\mathrm{kg_f/W})$';

    end

    ylabel( ...
        effLabel, ...
        'Interpreter','latex', ...
        'FontSize',fontSize);

    set(ax, ...
        'FontSize',fontSize, ...
        'TickLabelInterpreter','latex');

    addPlotTitles( ...
        ax, ...
        '$\mathrm{Thrust\ Efficiency\ vs.\ ESC\ Command}$', ...
        subtitleText, ...
        titleSize, ...
        subtitleSize);
end


%% ========================================================================
% Helper Functions
% ========================================================================

function name = findColumn(T, aliases)
% FINDCOLUMN finds a matching table column from a list of possible names.

    variableNames = T.Properties.VariableNames;
    name = '';

    % Exact match first
    for i = 1:numel(aliases)

        idx = strcmp(variableNames, aliases{i});

        if any(idx)
            name = variableNames{find(idx,1)};
            return;
        end
    end

    % Case-insensitive match
    for i = 1:numel(aliases)

        idx = strcmpi(variableNames, aliases{i});

        if any(idx)
            name = variableNames{find(idx,1)};
            return;
        end
    end
end


function txt = escapeLatex(txt)
% ESCAPELATEX prepares user-entered text for MATLAB's LaTeX interpreter.

    txt = strrep(txt, '\', '\textbackslash ');
    txt = strrep(txt, '_', '\_');
    txt = strrep(txt, '%', '\%');
    txt = strrep(txt, '&', '\&');
    txt = strrep(txt, '#', '\#');
    txt = strrep(txt, '$', '\$');
    txt = strrep(txt, '{', '\{');
    txt = strrep(txt, '}', '\}');

    % Preserve spaces in LaTeX math mode
    txt = strrep(txt, ' ', '~');
end


function addPlotTitles(ax, mainTitle, secondaryTitle, ...
                       titleSize, subtitleSize)

    % Prevent MATLAB from automatically scaling the title
    ax.TitleFontSizeMultiplier = 1;

    % Main title
    hTitle = title(ax, mainTitle, ...
        'Interpreter','latex', ...
        'FontWeight','bold');

    % Secondary motor / propeller line
    hSubtitle = subtitle(ax, secondaryTitle, ...
        'Interpreter','latex', ...
        'FontWeight','normal');

    % Explicitly set sizes after both objects exist
    hTitle.FontSize = titleSize;
    hSubtitle.FontSize = subtitleSize;

end