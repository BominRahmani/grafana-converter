// This file is generated, do not manually edit.
{
  '#': { help: 'grafonnet.alerting.notificationPolicy', name: 'notificationPolicy' },
  '#withContinue': { 'function': { args: [{ default: true, enums: null, name: 'value', type: ['boolean'] }], help: 'A Route is a node that contains definitions of how to handle alerts. This is modified\nfrom the upstream alertmanager in that it adds the ObjectMatchers property.' } },
  withContinue(value=true): {
    continue: value,
  },
  '#withGroupInterval': { 'function': { args: [{ default: null, enums: null, name: 'value', type: ['string'] }], help: 'A Route is a node that contains definitions of how to handle alerts. This is modified\nfrom the upstream alertmanager in that it adds the ObjectMatchers property.' } },
  withGroupInterval(value): {
    group_interval: value,
  },
  '#withGroupWait': { 'function': { args: [{ default: null, enums: null, name: 'value', type: ['string'] }], help: 'A Route is a node that contains definitions of how to handle alerts. This is modified\nfrom the upstream alertmanager in that it adds the ObjectMatchers property.' } },
  withGroupWait(value): {
    group_wait: value,
  },
  '#withRepeatInterval': { 'function': { args: [{ default: null, enums: null, name: 'value', type: ['string'] }], help: 'A Route is a node that contains definitions of how to handle alerts. This is modified\nfrom the upstream alertmanager in that it adds the ObjectMatchers property.' } },
  withRepeatInterval(value): {
    repeat_interval: value,
  },
  '#withGroupBy': { 'function': { args: [{ default: null, enums: null, name: 'value', type: ['array'] }], help: 'A Route is a node that contains definitions of how to handle alerts. This is modified\nfrom the upstream alertmanager in that it adds the ObjectMatchers property.' } },
  withGroupBy(value): {
    group_by:
      (if std.isArray(value)
       then value
       else [value]),
  },
  '#withGroupByMixin': { 'function': { args: [{ default: null, enums: null, name: 'value', type: ['array'] }], help: 'A Route is a node that contains definitions of how to handle alerts. This is modified\nfrom the upstream alertmanager in that it adds the ObjectMatchers property.' } },
  withGroupByMixin(value): {
    group_by+:
      (if std.isArray(value)
       then value
       else [value]),
  },
  '#withMatchers': { 'function': { args: [{ default: null, enums: null, name: 'value', type: ['array'] }], help: 'Matchers is a slice of Matchers that is sortable, implements Stringer, and\nprovides a Matches method to match a LabelSet against all Matchers in the\nslice. Note that some users of Matchers might require it to be sorted.' } },
  withMatchers(value): {
    matchers:
      (if std.isArray(value)
       then value
       else [value]),
  },
  '#withMatchersMixin': { 'function': { args: [{ default: null, enums: null, name: 'value', type: ['array'] }], help: 'Matchers is a slice of Matchers that is sortable, implements Stringer, and\nprovides a Matches method to match a LabelSet against all Matchers in the\nslice. Note that some users of Matchers might require it to be sorted.' } },
  withMatchersMixin(value): {
    matchers+:
      (if std.isArray(value)
       then value
       else [value]),
  },
  '#withMuteTimeIntervals': { 'function': { args: [{ default: null, enums: null, name: 'value', type: ['array'] }], help: 'A Route is a node that contains definitions of how to handle alerts. This is modified\nfrom the upstream alertmanager in that it adds the ObjectMatchers property.' } },
  withMuteTimeIntervals(value): {
    mute_time_intervals:
      (if std.isArray(value)
       then value
       else [value]),
  },
  '#withMuteTimeIntervalsMixin': { 'function': { args: [{ default: null, enums: null, name: 'value', type: ['array'] }], help: 'A Route is a node that contains definitions of how to handle alerts. This is modified\nfrom the upstream alertmanager in that it adds the ObjectMatchers property.' } },
  withMuteTimeIntervalsMixin(value): {
    mute_time_intervals+:
      (if std.isArray(value)
       then value
       else [value]),
  },
  '#withReceiver': { 'function': { args: [{ default: null, enums: null, name: 'value', type: ['string'] }], help: 'A Route is a node that contains definitions of how to handle alerts. This is modified\nfrom the upstream alertmanager in that it adds the ObjectMatchers property.' } },
  withReceiver(value): {
    receiver: value,
  },
  '#withRoutes': { 'function': { args: [{ default: null, enums: null, name: 'value', type: ['array'] }], help: 'A Route is a node that contains definitions of how to handle alerts. This is modified\nfrom the upstream alertmanager in that it adds the ObjectMatchers property.' } },
  withRoutes(value): {
    routes:
      (if std.isArray(value)
       then value
       else [value]),
  },
  '#withRoutesMixin': { 'function': { args: [{ default: null, enums: null, name: 'value', type: ['array'] }], help: 'A Route is a node that contains definitions of how to handle alerts. This is modified\nfrom the upstream alertmanager in that it adds the ObjectMatchers property.' } },
  withRoutesMixin(value): {
    routes+:
      (if std.isArray(value)
       then value
       else [value]),
  },
  matcher+:
    {
      '#': { help: '', name: 'matcher' },
      '#withName': { 'function': { args: [{ default: null, enums: null, name: 'value', type: ['string'] }], help: '' } },
      withName(value): {
        Name: value,
      },
      '#withType': { 'function': { args: [{ default: null, enums: ['=', '!=', '=~', '!~'], name: 'value', type: ['string'] }], help: '' } },
      withType(value): {
        Type: value,
      },
      '#withValue': { 'function': { args: [{ default: null, enums: null, name: 'value', type: ['string'] }], help: '' } },
      withValue(value): {
        Value: value,
      },
    },
}
+ (import '../../custom/alerting/notificationPolicy.libsonnet')
