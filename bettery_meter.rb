#!/usr/bin/env ruby
#############################################################
# Author: Robert Jorgenson <rjorgenson@gmail.com>
#
# Usage: Please see README for usage details
#
# License: Free! Do whatever you want with it =]
#############################################################
#require 'rubygems'
#require 'term/ansicolor'
#############################################################
# Returns battery status/info
#############################################################
class Color
  attr_accessor :red,:yellow,:green,:clear,:rapid_blink
  def initialize()
    @red = "\e[31m"
    @yellow = "\e[33m"
    @green = "\e[32m"
    @clear = "\e[0m"
    @rapid_blink = "\e[6m"
  end
end
class Battery
  attr_accessor :percent
  def initialize(color = true) # gather relevant info
    @conn = `ioreg -n AppleSmartBattery | grep ExternalConnected | awk '{ print $5 }'`.strip == "Yes" # is power connected
    @chrg = `ioreg -n AppleSmartBattery | grep IsCharging | awk '{ print $5 }'`.strip == "Yes"       # is battery chargin
    @time = `ioreg -n AppleSmartBattery | grep TimeRemaining | awk '{ print $5 }'`              # time remaining on battery
    @max = `ioreg -n AppleSmartBattery | grep MaxCapacity | awk '{ print $5 }'`                 # maximum capacity
    @cur = `ioreg -n AppleSmartBattery | grep CurrentCapacity | awk '{ print $5 }'`             # current capacity
    @full = `ioreg -n AppleSmartBattery | grep FullyCharged | awk '{ print $5 }'`.strip == "Yes"      # is battery full
    @color = color ? Color.new : nil
    @percent = (@cur.to_f / @max.to_f * 100).round.to_i
  end # def initialize

  def build_meter(full = "❚", empty = "·") # built battery meter
    meter = ""
    10.step(100, 10) do |i| # one bar per 10% battery, dashes for each empty 10%
      case i
        when 0..20: meter << @color.red       # first 2 bars red
        when 30..50: meter << @color.yellow   # next 3 bars yellow
        else meter << @color.green            # remaining 5 green
      end
      if i <= @percent
        meter << full + @color.clear # clear color
      else
        meter << empty # empty
      end
    end # end for loop
    return meter + @color.clear
  end # def build_meter
  
  def build_time # determines time remaining on battery
    hour = @time.strip.to_i / 60 # hours left
    min = @time.strip.to_i - (hour * 60) # minutes left
    min < 10 ? min = "0#{min}" : nil # make sure minutes is two digits long
    ret_string = ""
    
    if @conn then # power cable connected
      if @chrg then # is plugged in and charging
        ret_string << "Charging: #{hour}:#{min}"
      else # is plugged in but not charging
        ret_string << (@full ? "Charged" : "Not Charging")
      end # if @chrg.strip == "Yes"
    else # power is not connected
      if @time.to_i < 1 || @time.to_i > 600 then
        ret_string << "Calculating"
      else
        ret_string << "Remaining: "
        case @time.to_i
          when 0..30: ret_string << @color.red + @color.rapid_blink
          when 31..60: ret_string << @color.yellow
        end
        ret_string << "#{hour}:#{min}" + @color.clear
      end # if @time < 1 || @ time > 2000 
    end # if @conn.strip == "Yes"
    
    return ret_string
  end # def build_time
end # Class Battery

#############################################################
# Script execution
#############################################################
batt = Battery.new
if ARGV.length > 0 then
    puts batt.build_meter.to_s + " " + batt.percent.to_s + "%"
else
    puts batt.build_meter.to_s + " " + batt.percent.to_s + "%\n" + batt.build_time.to_s
end
