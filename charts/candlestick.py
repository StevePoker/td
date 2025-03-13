from api_manager.hepler.TimeFormatter import TimeConverter


class CandleStick:
    @staticmethod
    def create(fig, row_pos, col_pos, data, range_size):
        for index, row in data.iterrows():
            if index in range(500-range_size):
                continue
            fig.add_shape(type='line', y0=row['h'], y1=row['l'],
                          x0=TimeConverter.sec_to_date(row['ot'], 7200), x1=TimeConverter.sec_to_date(row['ot'], 7200),
                          line=dict(color='Black', width=1)
                          )
            if row['c'] > row['o']:
                fig.add_shape(type='rect', xsizemode='pixel',
                              y0=row['o'], y1=row['c'], xanchor=TimeConverter.sec_to_date(row['ot'], 7200),
                              x0=-4, x1=4,
                              row=row_pos, col=col_pos,
                              line=dict(
                                  color="Black",
                                  width=2,
                              ),
                              fillcolor="White",
                              )
            elif row['c'] < row['o']:
                fig.add_shape(type='rect', xsizemode='pixel',
                              y0=row['o'], y1=row['c'], xanchor=TimeConverter.sec_to_date(row['ot'], 7200),
                              x0=-3, x1=3,
                              row=row_pos, col=col_pos,
                              line=dict(
                                  color="Black",
                                  width=2,
                              ),
                              fillcolor="Black",
                              )
            else:
                fig.add_shape(type='rect', xsizemode='pixel',
                              y0=row['o'], y1=row['c'], xanchor=TimeConverter.sec_to_date(row['ot'], 7200),
                              x0=-3, x1=3,
                              row=row_pos, col=col_pos,
                              line=dict(
                                  color="Yellow",
                                  width=2,
                              ),
                              fillcolor="Yellow",
                              )
