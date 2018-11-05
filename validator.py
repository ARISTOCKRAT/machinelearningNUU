"""Here we validate values"""
import error_handler


def metric(metric_name):
    import settings

    if metric_name:
        if type(metric_name) is int:
            if metric_name < 1 or metric_name > 7:
                error_handler.write(f"ERROR:\t out of range:: continue working as default::"
                                    f"\n\tmetric type({metric_name}) is {type(metric_name)}")
                return settings.metric.default_metric
            else:
                return metric_name
        elif type(metric_name) is float:
            metric(int(metric_name))
        elif type(metric_name) is str:
            metric_name = metric_name.lower()
            for item in settings.metric.metric_dict.items():
                if metric_name == item[1]:
                    return item[0]
            else:
                error_handler.write(f"ERROR:\t out of range:: continue working as default::"
                                    f"\n\tmetric type({metric_name}) is {type(metric_name)}")
                return settings.metric.default_metric

        elif type(metric_name) is list or type(metric_name) is tuple:
            metric(metric_name[0])
        elif type(metric_name) is dict:
            for el in metric_name.items():
                return metric(el[1])
        elif type(metric_name) is set:
            for el in metric_name:
                return metric(el)
        else:
            error_handler.write(f"ERROR:\t unresolved type of value::\n\t"
                                f"metric type({metric_name}) is {type(metric_name)}")
    else:
        if metric_name is None:
            import settings
            return settings.metric.default_metric
        error_handler.write(f"ERROR:\t invalid value:: continue working as default::\n\t"
                            f"metric type({metric_name}) is {type(metric_name)}")

    return settings.metric.default_metric

