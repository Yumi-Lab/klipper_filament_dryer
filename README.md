# Klipper Filament Dryer

## Introduction

Module for YMS dryers

## Sample Config

<pre>[filament_dryer YMS-1]
heater: YMS-1
auto_target_temp: 45  # Température automatique par défaut si besoin
manual_target_temp: 45  # Température pour commande DRY_FILAMENT si pas de TEMP spécifié
default_manual_dry_time: 60  # Durée par défaut en minutes si pas précisé


[heater_generic YMS-1]
heater_pin: smartbox:PC8 
sensor_type: EPCOS 100K B57560G104F #ATC Semitec 104GT-2
sensor_pin: smartbox:PC1
#sensor_list: temperature_sensor dryer_sensor
#maximum_deviation: 999
#combination_method: min
max_power: 1
control: pid #watermark
pid_Kp: 50
pid_Ki: 50
pid_Kd: 50
#kick_start_time: 0.5
#pwm_cycle_time:
#max_delta: 3.0
min_temp: -50
max_temp: 110</pre>

## Requirements

- Heater

## Macros

<pre>[gcode_macro START_DRYER_YMS1]
description: "Démarrer séchage YMS-1 avec température et minutes personnalisées"
gcode:
    {% set target_temp = params.TEMP|default(45)|float %}
    {% set minutes = params.MINUTES|default(60)|float %}

    DRY_FILAMENT MINUTES={minutes|int} TEMP={target_temp|int}


[gcode_macro STOP_DRYER_YMS1]
description: "Arrêter manuellement le sèche-filament YMS-1"
gcode:
    STOP_FILAMENT_DRYER
    M118 Dryer : Séchage arrêté manuellement.</pre>



## Install

<pre>cd ~
git clone https://github.com/Turge08/klipper_filament_dryer
cd klipper_filament_dryer
./install.sh</pre>

## Removal

<pre>cd ~
sudo rm -r ~/klipper_filament_dryer
sudo rm -r ~/klipper/klippy/extras/filament_dryer.py</pre>

